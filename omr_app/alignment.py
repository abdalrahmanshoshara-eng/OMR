"""Sheet alignment.

The current answer sheet has no fiducial markers, so alignment uses the printed
content itself:

1. Global: ORB keypoints (text, table header, score box) matched to the reference
   render -> RANSAC homography. Handles rotation (any angle, incl. upside-down),
   translation, scaling / DPI differences and mild perspective.
2. Local: every printed 'O' glyph is template-matched in a small window around its
   predicted position; an affine correction is fitted on the empty (matchable)
   bubbles and applied to all 40 bubbles (filled bubbles cannot be matched, they
   inherit the fitted correction).

Everything is deterministic (fixed ORB parameters, RANSAC with fixed seed).
"""
import logging
import math
from dataclasses import dataclass, field

import cv2
import numpy as np

log = logging.getLogger("omr_app.alignment")


@dataclass
class AlignmentResult:
    ok: bool
    warped: np.ndarray = None  # input warped into reference frame (gray)
    centers: dict = field(default_factory=dict)  # (q, opt) -> (x, y) refined positions
    info: dict = field(default_factory=dict)
    error: str = None
    low_confidence: bool = False


class Aligner:
    def __init__(self, layout, cfg: dict):
        self.layout = layout
        self.cfg = cfg
        self.orb = cv2.ORB_create(nfeatures=int(cfg["orb_max_features"]), scaleFactor=1.2, nlevels=8)
        self.ref = layout.ref_gray
        self.ref_kp, self.ref_desc = self.orb.detectAndCompute(self.ref, None)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    # ------------------------------------------------------------------ global
    def _homography(self, small):
        kp, desc = self.orb.detectAndCompute(small, None)
        if desc is None or len(kp) < 10:
            return None, {"keypoints": 0 if kp is None else len(kp)}, "no image features found (blank or unreadable image)"
        knn = self.matcher.knnMatch(desc, self.ref_desc, k=2)
        ratio = self.cfg["ratio_test"]
        good = [m for m, *rest in knn if rest and m.distance < ratio * rest[0].distance]
        info = {"keypoints": len(kp), "good_matches": len(good)}
        if len(good) < self.cfg["min_inliers"]:
            return None, info, f"too few feature matches with the reference sheet ({len(good)})"
        src = np.float32([kp[m.queryIdx].pt for m in good])
        dst = np.float32([self.ref_kp[m.trainIdx].pt for m in good])
        cv2.setRNGSeed(12345)
        H, mask = cv2.findHomography(src, dst, cv2.RANSAC, self.cfg["ransac_reproj_px"], maxIters=5000, confidence=0.999)
        if H is None:
            return None, info, "homography estimation failed"
        inl = int(mask.sum())
        info.update(inliers=inl, inlier_ratio=round(inl / len(good), 3))
        if inl < self.cfg["min_inliers"] or inl / len(good) < self.cfg["min_inlier_ratio"]:
            return None, info, f"sheet not recognised: only {inl} consistent feature matches"
        return H, info, None

    def _validate(self, H, small_shape, info):
        # local linear part around the answer area centre
        ax0, ay0, ax1, ay1 = self.layout.answer_area_px
        Hinv = np.linalg.inv(H)
        c = np.array([(ax0 + ax1) / 2, (ay0 + ay1) / 2, 1.0])
        eps = 20.0
        pts = np.array([c, c + [eps, 0, 0], c + [0, eps, 0]]).T
        q = Hinv @ pts
        q = q[:2] / q[2]
        J = np.column_stack([(q[:, 1] - q[:, 0]) / eps, (q[:, 2] - q[:, 0]) / eps])  # d(input)/d(ref)
        if np.linalg.det(J) <= 0:
            return "sheet appears mirrored (invalid transform)"
        sv = np.linalg.svd(J, compute_uv=False)
        scale = float(math.sqrt(sv[0] * sv[1]))
        aniso = float(sv[0] / sv[1] - 1)
        rot = float(math.degrees(math.atan2(J[1, 0], J[0, 0])))
        info.update(scale=round(scale, 3), anisotropy=round(aniso, 3), rotation_deg=round(rot, 2))
        if not self.cfg["min_scale"] <= scale <= self.cfg["max_scale"]:
            return f"implausible sheet scale ({scale:.2f}) - sheet too small in the image or not this sheet"
        if aniso > self.cfg["max_anisotropy"]:
            return f"sheet too distorted (anisotropy {aniso:.2f})"
        # the answer area must be fully inside the input image
        h, w = small_shape[:2]
        corners = np.array([[ax0, ay0, 1], [ax1, ay0, 1], [ax1, ay1, 1], [ax0, ay1, 1]], float).T
        pc = Hinv @ corners
        pc = pc[:2] / pc[2]
        margin = -2
        inside = (pc[0] >= margin) & (pc[0] <= w - 1 - margin) & (pc[1] >= margin) & (pc[1] <= h - 1 - margin)
        if not inside.all():
            return "answer area is cut off / outside the image (cropped or incomplete scan)"
        return None

    # ------------------------------------------------------------------ local
    def _match_glyphs(self, warped, search_pt):
        L = self.layout
        half = L.patch_half_px
        sr = int(round(search_pt * L.dpi / 72))
        tmpl = L.glyph_patch
        src, meas, scores, keys = [], [], [], []
        for b in L.bubbles:
            x, y = (int(round(v)) for v in b.center)
            win = warped[max(0, y - half - sr): y + half + sr + 1, max(0, x - half - sr): x + half + sr + 1]
            if win.shape[0] < tmpl.shape[0] or win.shape[1] < tmpl.shape[1]:
                continue
            res = cv2.matchTemplate(win, tmpl, cv2.TM_CCOEFF_NORMED)
            _, score, _, loc = cv2.minMaxLoc(res)
            ox, oy = max(0, x - half - sr), max(0, y - half - sr)
            keys.append((b.question, b.option))
            src.append(b.center)
            meas.append((ox + loc[0] + half, oy + loc[1] + half))
            scores.append(score)
        return keys, np.float32(src), np.float32(meas), np.float32(scores)

    def _refine(self, warped):
        """Locate the printed 'O' glyphs and fit a correction (homography, or affine if few points).

        Tries the normal search radius first, then a wide one (for sheets where the global
        homography is less precise, e.g. strong perspective / low resolution).
        """
        L = self.layout
        rc = self.cfg["refine"]
        centers = {(b.question, b.option): tuple(b.center) for b in L.bubbles}
        for search_pt in (rc["search_radius_pt"], rc.get("wide_search_radius_pt", rc["search_radius_pt"])):
            keys, src, meas, scores = self._match_glyphs(warped, search_pt)
            good = scores >= rc["min_match_score"]
            if good.sum() >= rc["min_matched_bubbles"]:
                break
        info = {"glyph_matches": int(good.sum()), "glyph_search_pt": search_pt,
                "glyph_match_median": round(float(np.median(scores[good])), 3) if good.any() else 0.0}
        if good.sum() < rc["min_matched_bubbles"]:
            info["refine"] = "failed (not enough printed bubbles found - positions cannot be verified)"
            return centers, info, True
        cv2.setRNGSeed(12345)
        thr = rc["max_residual_px"]
        Hm, _ = cv2.findHomography(src[good], meas[good], cv2.RANSAC, thr, maxIters=2000, confidence=0.999)
        if Hm is not None:
            fitted = cv2.perspectiveTransform(src.reshape(-1, 1, 2), Hm).reshape(-1, 2)
            info["refine_model"] = "homography"
        else:
            M, _ = cv2.estimateAffine2D(src[good], meas[good], method=cv2.RANSAC, ransacReprojThreshold=thr, maxIters=2000, confidence=0.999, refineIters=10)
            if M is None:
                info["refine"] = "fit failed"
                return centers, info, True
            fitted = np.hstack([src, np.ones((len(src), 1), np.float32)]) @ M.T
            info["refine_model"] = "affine"
        resid = np.linalg.norm(fitted - meas, axis=1)
        if (good & (resid <= thr)).sum() < rc["min_matched_bubbles"]:
            info["refine"] = "failed (printed bubbles inconsistent with a single sheet transform)"
            return centers, info, True
        inl_mask = good & (resid <= rc["max_residual_px"])
        info["residual_px"] = round(float(np.sqrt(np.mean(resid[inl_mask] ** 2))) if inl_mask.any() else 0.0, 2)
        info["refine_shift_px"] = round(float(np.median(np.linalg.norm(fitted - src, axis=1))), 2)
        for i, k in enumerate(keys):
            # measured position when the glyph matched well and agrees with the model, else the model
            centers[k] = tuple(map(float, meas[i] if inl_mask[i] else fitted[i]))
        info["refine"] = "ok"
        return centers, info, False

    # ------------------------------------------------------------------ main
    def align(self, gray: np.ndarray) -> AlignmentResult:
        rw, rh = self.layout.size
        h, w = gray.shape[:2]
        s = math.sqrt((rw * rh) / float(w * h))
        small = cv2.resize(gray, (max(1, int(round(w * s))), max(1, int(round(h * s)))), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        small = cv2.normalize(small, None, 0, 255, cv2.NORM_MINMAX)
        H, info, err = self._homography(small)
        info["work_scale"] = round(s, 4)
        if err:
            return AlignmentResult(ok=False, info=info, error=err)
        err = self._validate(H, small.shape, info)
        if err:
            return AlignmentResult(ok=False, info=info, error=err)
        warped = cv2.warpPerspective(small, H, (rw, rh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=255)
        if self.cfg["refine"].get("enabled", True):
            centers, rinfo, low = self._refine(warped)
        else:
            centers, rinfo, low = {(b.question, b.option): b.center for b in self.layout.bubbles}, {"refine": "disabled"}, False
        info.update(rinfo)
        info["method"] = "orb_homography+glyph_affine_refine"
        return AlignmentResult(ok=True, warped=warped, centers=centers, info=info, low_confidence=low)
