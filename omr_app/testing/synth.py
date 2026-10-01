"""Synthetic filled-sheet generator used to build the test dataset.

Renders the real blank answer sheet PDF, draws hand-like pen marks into the bubbles
and applies scanner / camera degradations. Deterministic for a given seed.

NOTE: synthetic data validates the pipeline logic and robustness to geometric /
photometric distortions; it does NOT replace testing on real scanned sheets.
"""
import math

import cv2
import numpy as np

from omr_app.imaging import render_pdf_page

OPTIONS = ["A", "B", "C", "D"]


def bubble_center_pt(q, opt, sheet_cfg_template):
    """Bubble centre in PDF points, from the OMRChecker template (pixels @ reference dpi)."""
    t, dpi = sheet_cfg_template
    fb = t["fieldBlocks"]["MCQ"]
    bw, bh = t["bubbleDimensions"]
    x = fb["origin"][0] + OPTIONS.index(opt) * fb["bubblesGap"] + bw / 2
    y = fb["origin"][1] + (q - 1) * fb["labelsGap"] + bh / 2
    return x * 72 / dpi, y * 72 / dpi


class SheetSynth:
    def __init__(self, pdf_path, template, ref_dpi, dpi=200, seed=0):
        self.dpi = dpi
        self.k = dpi / 72.0
        self.blank = render_pdf_page(pdf_path, 0, dpi)
        self.tpl = (template, ref_dpi)
        self.rng = np.random.default_rng(seed)

    def pt(self, v):
        return v * self.k

    # ------------------------------------------------------------------ marks
    def _mark_layer(self, shape):
        return np.full(shape, 255, np.uint8)

    def draw_mark(self, layer, q, opt, style="fill", ink=40, size=1.0):
        rng = self.rng
        cx, cy = bubble_center_pt(q, opt, self.tpl)
        cx, cy = self.pt(cx), self.pt(cy)
        cx += rng.normal(0, self.pt(0.5))
        cy += rng.normal(0, self.pt(0.5))
        ink = int(np.clip(ink + rng.normal(0, 6), 0, 250))
        if style in ("fill", "light", "overfill", "underfill"):
            base = {"fill": 5.0, "light": 5.0, "overfill": 7.0, "underfill": 3.6}[style] * size
            rx = self.pt(base * rng.uniform(0.92, 1.08))
            ry = self.pt(base * rng.uniform(0.92, 1.08))
            ang = rng.uniform(0, 180)
            cv2.ellipse(layer, (int(cx), int(cy)), (int(rx), int(ry)), ang, 0, 360, ink, -1, cv2.LINE_AA)
            # pen texture: scribble strokes leave small lighter streaks
            for _ in range(int(rng.integers(3, 7))):
                a = rng.uniform(0, math.pi)
                l = rx * rng.uniform(0.4, 0.9)
                ox, oy = rng.normal(0, rx * 0.25, 2)
                p1 = (int(cx + ox - l * math.cos(a)), int(cy + oy - l * math.sin(a)))
                p2 = (int(cx + ox + l * math.cos(a)), int(cy + oy + l * math.sin(a)))
                cv2.line(layer, p1, p2, int(min(255, ink + rng.uniform(15, 45))), 1, cv2.LINE_AA)
        elif style == "half":  # only part of the circle filled -> should be UNCERTAIN
            r = int(self.pt(4.8))
            a0 = rng.uniform(0, 360)
            cv2.ellipse(layer, (int(cx), int(cy)), (r, r), a0, 0, 120, ink, -1, cv2.LINE_AA)
        elif style == "tick":
            s = self.pt(4.5)
            pts = np.int32([[cx - s, cy], [cx - s * 0.3, cy + s * 0.8], [cx + s * 1.1, cy - s * 1.1]])
            cv2.polylines(layer, [pts], False, ink, max(2, int(self.pt(1.1))), cv2.LINE_AA)
        elif style == "cross":
            s = self.pt(4.5)
            t = max(2, int(self.pt(1.1)))
            cv2.line(layer, (int(cx - s), int(cy - s)), (int(cx + s), int(cy + s)), ink, t, cv2.LINE_AA)
            cv2.line(layer, (int(cx - s), int(cy + s)), (int(cx + s), int(cy - s)), ink, t, cv2.LINE_AA)
        elif style == "dot":  # stray pen dot -> must stay BLANK
            cv2.circle(layer, (int(cx + self.pt(1.5)), int(cy - self.pt(1))), int(self.pt(0.9)), ink, -1, cv2.LINE_AA)
        elif style == "erased":  # erased pencil residue -> light smear
            r = int(self.pt(5))
            cv2.circle(layer, (int(cx), int(cy)), r, 215, -1, cv2.LINE_AA)
        else:
            raise ValueError(style)

    def draw_handwriting(self, layer):
        """Scribbles in the name / specialization / date / signature fields (never in bubbles)."""
        rng = self.rng
        for (x0, x1, y) in [(125, 400, 141), (125, 330, 161), (125, 230, 181), (160, 250, 546), (160, 250, 568), (420, 470, 568)]:
            x = x0
            pts = []
            while x < x1:
                pts.append((self.pt(x), self.pt(y - 3 + rng.uniform(-4, 3))))
                x += rng.uniform(2, 5)
            cv2.polylines(layer, [np.int32(pts)], False, int(rng.uniform(30, 70)), 2, cv2.LINE_AA)

    def make_sheet(self, marks, handwriting=True):
        """marks: list of (q, opt, style, ink)."""
        layer = self._mark_layer(self.blank.shape)
        if handwriting:
            self.draw_handwriting(layer)
        for q, opt, style, ink in marks:
            self.draw_mark(layer, q, opt, style, ink)
        return np.minimum(self.blank, layer)

    # ------------------------------------------------------------------ degradations
    def degrade(self, img, rotate=0.0, scale=1.0, shift=(0, 0), perspective=0.0, brightness=0, contrast=1.0,
                gamma=1.0, noise=0.0, blur=0, jpeg=None, speckle=0, bed=True, gradient=0.0, crop=None):
        rng = self.rng
        h, w = img.shape
        pad = int(0.06 * max(h, w)) if bed else 0
        canvas = np.full((h + 2 * pad, w + 2 * pad), 255, np.uint8)
        canvas[pad:pad + h, pad:pad + w] = img
        if bed:  # scanner lid / bed shows as grey around the paper once rotated
            canvas = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=200)
        H, W = canvas.shape
        c = (W / 2, H / 2)
        M = cv2.getRotationMatrix2D(c, rotate, scale)
        M[:, 2] += shift
        M3 = np.vstack([M, [0, 0, 1]])
        if perspective:
            src = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
            d = perspective * W
            dst = np.float32([[rng.uniform(0, d), rng.uniform(0, d)], [W - rng.uniform(0, d), rng.uniform(0, d)],
                              [W - rng.uniform(0, d), H - rng.uniform(0, d)], [rng.uniform(0, d), H - rng.uniform(0, d)]])
            M3 = cv2.getPerspectiveTransform(src, dst) @ M3
        out = cv2.warpPerspective(canvas, M3, (W, H), flags=cv2.INTER_LINEAR, borderValue=200 if bed else 255)
        out = out.astype(np.float32)
        if gradient:
            gx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
            out = out * (1 - gradient * (gx + 1) / 2)
        out = (out / 255.0) ** gamma * 255.0
        out = (out - 128) * contrast + 128 + brightness
        if blur:
            out = cv2.GaussianBlur(out, (blur | 1, blur | 1), 0)
        if noise:
            out += rng.normal(0, noise, out.shape).astype(np.float32)
        out = np.clip(out, 0, 255).astype(np.uint8)
        if speckle:
            ys = rng.integers(0, H, speckle)
            xs = rng.integers(0, W, speckle)
            for x, y in zip(xs, ys):
                cv2.circle(out, (int(x), int(y)), int(rng.integers(1, 3)), int(rng.integers(0, 90)), -1)
        if crop is not None:
            x0, y0, x1, y1 = crop  # fractions
            out = out[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
        if jpeg:
            ok, buf = cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, int(jpeg)])
            out = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
        return out
