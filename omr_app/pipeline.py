"""End-to-end grading of one sheet image / file.

    Image/PDF -> preprocessing -> alignment -> bubble fill measurement
    -> classification -> answer key comparison -> score -> status

Every decision is recorded in the returned result dict (fill ratios per option,
thresholds used, alignment metrics, config fingerprint) so any score can be audited.
"""
import logging
import time
from pathlib import Path

import cv2
import numpy as np

from omr_app import __version__
from omr_app.alignment import Aligner
from omr_app.config import config_fingerprint, load_answer_keys, load_sheet_config, load_thresholds
from omr_app.detection import BLANK, MULTIPLE, UNCERTAIN, classify_question, ink_threshold, measure_bubbles
from omr_app.imaging import darkness_map, load_input
from omr_app.layout import load_layout
from omr_app.scoring import FAILED, REVIEW_REQUIRED, score_questions, sheet_status

log = logging.getLogger("omr_app.pipeline")

# BGR colours for the overlay
C_OK, C_WRONG, C_WARN, C_BLANK, C_EXPECTED = (60, 160, 40), (40, 40, 210), (0, 140, 255), (150, 150, 150), (200, 120, 0)


class Grader:
    def __init__(self, cfg_dir=None):
        self.cfg_dir = cfg_dir
        self.reload()

    def reload(self):
        self.sheet_cfg = load_sheet_config(self.cfg_dir)
        self.thresholds = load_thresholds(self.cfg_dir)
        self.layout = load_layout(self.sheet_cfg)
        self.aligner = Aligner(self.layout, self.sheet_cfg["alignment"])
        self.fingerprint = config_fingerprint(
            {k: v for k, v in self.sheet_cfg.items() if k != "_dir"}, self.thresholds
        )

    def answer_keys(self):
        return load_answer_keys(self.cfg_dir, self.layout.num_questions, self.layout.options)

    # ------------------------------------------------------------------ public
    def grade_file(self, path, answer_key, out_dir=None, candidate_id=None):
        """Grade every page of an image/PDF. Returns a list of result dicts."""
        path = Path(path)
        t0 = time.perf_counter()
        try:
            pages = load_input(path, self.thresholds["image"]["pdf_render_dpi"])
        except Exception as e:  # unreadable file -> one FAILED result
            log.error("%s: cannot read file: %s", path.name, e)
            r = self._failed(path, 1, candidate_id or path.stem, answer_key, f"cannot read file: {e}", {})
            r["processing_ms"] = round((time.perf_counter() - t0) * 1000, 1)
            return [r]
        results = []
        for page_no, gray in pages:
            cid = candidate_id or (path.stem if len(pages) == 1 else f"{path.stem}_p{page_no}")
            results.append(self.grade_image(gray, answer_key, source=path, page=page_no, candidate_id=cid, out_dir=out_dir))
        return results

    def grade_image(self, gray, answer_key, source="image", page=1, candidate_id=None, out_dir=None):
        t0 = time.perf_counter()
        source = Path(source)
        cid = candidate_id or source.stem
        h, w = gray.shape[:2]
        log.info("processing %s (page %d) %dx%d", source.name, page, w, h)
        img_info = {"width": w, "height": h}

        al = self.aligner.align(gray)
        if not al.ok:
            log.warning("%s p%d: alignment FAILED: %s", source.name, page, al.error)
            r = self._failed(source, page, cid, answer_key, al.error, al.info, img_info)
            r["processing_ms"] = round((time.perf_counter() - t0) * 1000, 1)
            return r
        a = al.info
        log.info(
            "%s p%d: aligned (inliers=%s, rot=%s deg, scale=%s, glyphs=%s/40, residual=%s px)%s",
            source.name, page, a.get("inliers"), a.get("rotation_deg"), a.get("scale"),
            a.get("glyph_matches"), a.get("residual_px"), " LOW CONFIDENCE" if al.low_confidence else "",
        )
        if al.low_confidence and self.thresholds["review"].get("fail_on_unverified_alignment", True):
            # never show answers read from unverified bubble positions
            err = f"bubble positions could not be verified: {a.get('refine')}"
            log.warning("%s p%d: FAILED: %s", source.name, page, err)
            r = self._failed(source, page, cid, answer_key, err, {**a, "low_confidence": True}, img_info)
            if out_dir is not None:
                out_dir = Path(out_dir)
                out_dir.mkdir(parents=True, exist_ok=True)
                p = out_dir / f"{_safe(cid)}_aligned.jpg"
                _imwrite(p, al.warped, [cv2.IMWRITE_JPEG_QUALITY, 92])
                r["artifacts"] = {"aligned": p.name, "overlay": p.name, "fields": {}}
            r["processing_ms"] = round((time.perf_counter() - t0) * 1000, 1)
            return r

        imcfg = self.thresholds["image"]
        dark = darkness_map(al.warped, imcfg["blur_ksize"], int(round(self.layout.pt_to_px(imcfg["illumination_kernel_pt"]))))
        thr, ink_level, paper_level = ink_threshold(dark, al.centers, self.layout, self.thresholds["fill"])
        meas = measure_bubbles(dark, al.centers, self.layout, self.thresholds["fill"], thr, paper_level)
        log.debug("%s p%d: paper %.2f, ink %.2f -> pixel ink threshold %.2f", source.name, page, paper_level, ink_level, thr)

        cls_th = self.thresholds["classification"]
        questions = []
        for q in range(1, self.layout.num_questions + 1):
            m = {o: meas[(q, o)] for o in self.layout.options}
            fills = {o: round(m[o]["fill"], 3) for o in self.layout.options}
            shapes = {o: m[o]["shape"] for o in self.layout.options}
            detected, reason, margin = classify_question(
                {o: {"fill": fills[o], "hole": m[o]["hole"], "shape": shapes[o], "hole_darkness": m[o]["hole_darkness"] - paper_level}
                 for o in self.layout.options}, cls_th
            )
            questions.append({
                "q": q,
                "fills": fills,
                "shapes": shapes,
                "hole": {o: round(m[o]["hole"], 3) for o in self.layout.options},
                "outer": {o: round(m[o]["outer"], 3) for o in self.layout.options},
                "hole_darkness": {o: round(m[o]["hole_darkness"], 3) for o in self.layout.options},
                "darkness": {o: round(meas[(q, o)]["darkness"], 3) for o in self.layout.options},
                "centers": {o: meas[(q, o)]["center"] for o in self.layout.options},
                "detected": detected,
                "reason": reason,
                "margin": margin,
                "override": None,
            })
            log.debug("  Q%-2d %s -> %s (%s)", q, " ".join(f"{o}={f:.2f}{'~' if shapes[o] == 'strokes' else ''}" for o, f in fills.items()), detected, reason)

        result = self._base(source, page, cid, answer_key, img_info)
        result["alignment"] = {**a, "ok": True, "low_confidence": al.low_confidence}
        result["ink"] = {"paper_level": round(paper_level, 3), "ink_level": round(ink_level, 3), "pixel_threshold": round(thr, 3)}
        result["questions"] = questions
        warnings = []
        if al.low_confidence:
            warnings.append("alignment refinement could not verify bubble positions")
        if abs(a.get("rotation_deg", 0)) > 90:
            warnings.append(f"sheet was upside-down (rotated {a['rotation_deg']} deg) - corrected")
        result["warnings"] = warnings
        self.finalize(result, answer_key, low_alignment=al.low_confidence)

        if out_dir is not None:
            result["artifacts"] = self._save_artifacts(al.warped, result, Path(out_dir))
        result["processing_ms"] = round((time.perf_counter() - t0) * 1000, 1)
        log.info(
            "%s p%d: answers %s -> score %s/%s [%s]%s",
            source.name, page, "".join(_short(v) for v in result["answers"].values()),
            result["score"], result["max_score"], result["status"],
            (" reasons: " + "; ".join(result["status_reasons"])) if result["status_reasons"] else "",
        )
        return result

    def finalize(self, result, answer_key, low_alignment=None):
        """(Re)compute score + status from questions (also used after manual review)."""
        if result.get("status") == FAILED and not result.get("questions"):
            return result
        if low_alignment is None:
            low_alignment = result.get("alignment", {}).get("low_confidence", False)
        result["answer_key_id"] = answer_key["id"]
        result["exam"] = answer_key["exam"]
        result["specialization"] = answer_key["specialization"]
        result.update(score_questions(result["questions"], answer_key))
        result["answers"] = {str(qd["q"]): qd["final"] for qd in result["questions"]}
        result["detected_answers"] = {str(qd["q"]): qd["detected"] for qd in result["questions"]}
        status, reasons = sheet_status(result["questions"], self.thresholds["review"], low_alignment)
        n_key, n_sheet = len(answer_key["answers"]), len(result["questions"])
        if n_key != n_sheet:
            reasons.append(f"answer key has {n_key} questions, sheet has {n_sheet}")
            status = REVIEW_REQUIRED
        if result.get("reviewed"):
            status = "MANUALLY_REVIEWED"
        result["status"], result["status_reasons"] = status, reasons
        return result

    # ------------------------------------------------------------------ helpers
    def _base(self, source, page, cid, answer_key, img_info):
        return {
            "schema_version": 1,
            "engine_version": __version__,
            "config_fingerprint": self.fingerprint,
            "sheet_layout": self.layout.sheet_id,
            "source_file": source.name,
            "page": page,
            "candidate_id": cid,
            "candidate_name": None,
            "answer_key_id": answer_key["id"] if answer_key else None,
            "exam": answer_key["exam"] if answer_key else None,
            "specialization": answer_key["specialization"] if answer_key else None,
            "image": img_info,
            "thresholds": self.thresholds,
            "reviewed": False,
        }

    def _failed(self, source, page, cid, answer_key, error, align_info, img_info=None):
        r = self._base(Path(source), page, cid, answer_key, img_info or {})
        r.update({
            "status": FAILED, "status_reasons": [error], "error": error,
            "alignment": {**align_info, "ok": False}, "questions": [], "answers": {},
            "detected_answers": {}, "score": None,
            "max_score": answer_key["scoring"]["total_score"] if answer_key else None,
            "correct_count": None, "warnings": [],
        })
        return r

    def _save_artifacts(self, warped, result, out_dir):
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = _safe(f"{result['candidate_id']}")
        aligned_path = out_dir / f"{stem}_aligned.jpg"
        overlay_path = out_dir / f"{stem}_overlay.jpg"
        _imwrite(aligned_path, warped, [cv2.IMWRITE_JPEG_QUALITY, 92])
        _imwrite(overlay_path, self.draw_overlay(warped, result), [cv2.IMWRITE_JPEG_QUALITY, 90])
        crops = {}
        for name, f in self.layout.fields_px.items():
            x0, y0, x1, y1 = f["rect_px"]
            p = out_dir / f"{stem}_field_{name}.png"
            _imwrite(p, warped[y0:y1, x0:x1])
            crops[name] = p.name
        return {"aligned": aligned_path.name, "overlay": overlay_path.name, "fields": crops}

    def draw_overlay(self, warped, result):
        vis = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)
        r = self.layout.roi_radius_px + 4
        for qd in result["questions"]:
            final = qd["final"]
            for o in self.layout.options:
                x, y = qd["centers"][o]
                f = qd["fills"][o]
                if final == o:
                    col = C_OK if qd["correct"] else C_WRONG
                    cv2.circle(vis, (x, y), r, col, 3)
                elif final in (MULTIPLE, UNCERTAIN) and f >= self.thresholds["classification"]["uncertain_min_fill"]:
                    cv2.circle(vis, (x, y), r, C_WARN, 3)
                else:
                    cv2.circle(vis, (x, y), r, C_BLANK, 1)
                if o == qd["expected"] and not qd["correct"]:
                    cv2.circle(vis, (x, y), r + 5, C_EXPECTED, 1, cv2.LINE_AA)
                cv2.putText(vis, f"{int(round(f * 100))}", (x + r + 3, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (90, 90, 90), 1, cv2.LINE_AA)
            tag = {BLANK: "BLANK", MULTIPLE: "MULTI", UNCERTAIN: "UNSURE"}.get(final)
            y = qd["centers"][self.layout.options[0]][1]
            mark = "OK" if qd["correct"] else "X"
            cv2.putText(vis, tag or mark, (self.layout.answer_area_px[2] - 70, y + 6), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                        C_WARN if final in (MULTIPLE, UNCERTAIN) else (C_OK if qd["correct"] else C_WRONG), 2, cv2.LINE_AA)
        return vis


def _short(v):
    return {BLANK: "_", MULTIPLE: "*", UNCERTAIN: "?"}.get(v, v)


def _imwrite(path, img, params=()):
    # cv2.imwrite mangles non-ASCII (e.g. Arabic) paths on Windows; encode in memory and write via Python
    ok, buf = cv2.imencode(Path(path).suffix, img, list(params))
    if not ok:
        raise OSError(f"cannot encode image: {path}")
    Path(path).write_bytes(buf.tobytes())


def _safe(s):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in s)[:120]
