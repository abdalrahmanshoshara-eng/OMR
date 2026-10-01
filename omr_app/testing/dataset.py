"""Generate the synthetic test dataset with expected results.

    python -m omr_app.testing.dataset --out tests/dataset

Writes images / PDFs plus ``manifest.json``. Each entry has the expected status and,
per question, the expected classification (A-D / BLANK / MULTIPLE / UNCERTAIN).
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from omr_app.config import REPO_ROOT, load_answer_keys, load_sheet_config
from omr_app.testing.synth import OPTIONS, SheetSynth

KEYS = ["institute_2026_business_management", "institute_2026_commercial_banking", "institute_2026_applied_statistics"]


def _wrong(a, rng):
    return str(rng.choice([o for o in OPTIONS if o != a]))


class Builder:
    def __init__(self, out: Path, seed=2026):
        self.out = out
        self.out.mkdir(parents=True, exist_ok=True)
        cfg = load_sheet_config()
        cfg_dir = Path(cfg["_dir"])
        self.template = json.loads((cfg_dir / cfg["omr_template"]).read_text())
        self.pdf = cfg_dir / cfg["reference"]["pdf"]
        self.ref_dpi = cfg["reference"]["dpi"]
        self.keys = load_answer_keys()
        self.rng = np.random.default_rng(seed)
        self.entries = []
        self.n = 0
        self._synth = {}

    def synth(self, dpi):
        if dpi not in self._synth:
            self._synth[dpi] = SheetSynth(self.pdf, self.template, self.ref_dpi, dpi=dpi, seed=int(self.rng.integers(1 << 30)))
        return self._synth[dpi]

    def sheet(self, key_id, plan, dpi=200, ink=40, degrade=None):
        """plan: {q: ("B","fill") | [("A","fill"),("B","fill")] | None}; returns (image, expected)."""
        syn = self.synth(dpi)
        marks = []
        for q in range(1, 11):
            items = plan.get(q)
            if items is None:
                continue
            if isinstance(items, tuple):
                items = [items]
            for it in items:
                opt, style = it[0], it[1]
                marks.append((q, opt, style, it[2] if len(it) > 2 else ink))
        img = syn.make_sheet(marks)
        img = syn.degrade(img, **(degrade or {}))
        return img

    def add(self, category, name, img, key_id, expected, expected_status, note="", ext=".jpg"):
        self.n += 1
        fname = f"{self.n:03d}_{category}_{name}{ext}"
        path = self.out / fname
        if ext == ".jpg":
            cv2.imwrite(str(path), img, [cv2.IMWRITE_JPEG_QUALITY, 92])
        else:
            cv2.imwrite(str(path), img)
        self.entries.append({"file": fname, "category": category, "answer_key_id": key_id, "pages": [
            {"page": 1, "expected_answers": expected, "expected_status": expected_status, "note": note}]})

    def expected_from_plan(self, plan, overrides=None):
        exp = {}
        for q in range(1, 11):
            items = plan.get(q)
            if items is None:
                exp[str(q)] = "BLANK"
            elif isinstance(items, list):
                real = [i for i in items if i[1] not in ("dot", "erased")]
                exp[str(q)] = "MULTIPLE" if len(real) > 1 else real[0][0]
            else:
                exp[str(q)] = "BLANK" if items[1] in ("dot", "erased") else items[0]
        exp.update(overrides or {})
        return exp


def build(out: Path):
    b = Builder(out)
    rng = b.rng
    keys = b.keys

    def correct_plan(kid, style="fill", ink=None):
        return {int(q): ((a, style) if ink is None else (a, style, ink)) for q, a in keys[kid]["answers"].items()}

    def random_plan(style="fill"):
        return {q: (str(rng.choice(OPTIONS)), style) for q in range(1, 11)}

    mild = dict(rotate=0.7, noise=3, blur=3, jpeg=90)

    # 1. all correct (each specialization)
    for kid in KEYS:
        for i in range(2):
            p = correct_plan(kid)
            b.add("01_all_correct", f"{kid.split('_', 2)[2]}_{i}", b.sheet(kid, p, degrade={**mild, "rotate": float(rng.uniform(-1, 1))}),
                  kid, b.expected_from_plan(p), "AUTO_APPROVED")
    # 2. wrong answers
    for i in range(4):
        kid = KEYS[i % 3]
        p = correct_plan(kid)
        for q in rng.choice(np.arange(1, 11), size=int(rng.integers(2, 7)), replace=False):
            p[int(q)] = (_wrong(p[int(q)][0], rng), "fill")
        b.add("02_wrong_answers", str(i), b.sheet(kid, p, degrade=mild), kid, b.expected_from_plan(p), "AUTO_APPROVED")
    # 3. blank question(s)
    for i, blanks in enumerate([[4], [1, 10], [2, 5, 7], list(range(1, 11))]):
        kid = KEYS[i % 3]
        p = correct_plan(kid)
        for q in blanks:
            p[q] = None
        b.add("03_blank", f"{len(blanks)}blank", b.sheet(kid, p, degrade=mild), kid, b.expected_from_plan(p),
              "REVIEW_REQUIRED" if len(blanks) == 10 else "AUTO_APPROVED")
    # 4. multiple answers
    for i in range(3):
        kid = KEYS[i % 3]
        p = correct_plan(kid)
        q = int(rng.integers(1, 11))
        a = p[q][0]
        p[q] = [(a, "fill"), (_wrong(a, rng), "fill")]
        if i == 2:
            p[1] = [("A", "fill"), ("B", "fill"), ("C", "fill")] if q != 1 else p[1]
        b.add("04_multiple", str(i), b.sheet(kid, p, degrade=mild), kid, b.expected_from_plan(p), "REVIEW_REQUIRED")
    # 5. light marks (pencil / light pen)
    for i, ink in enumerate([120, 140, 155]):
        kid = KEYS[i % 3]
        p = correct_plan(kid, "light", ink)
        b.add("05_light_mark", f"ink{ink}", b.sheet(kid, p, degrade=mild), kid, b.expected_from_plan(p), "AUTO_APPROVED")
    # 6. very dark / over-filled marks
    for i in range(2):
        kid = KEYS[i % 3]
        p = correct_plan(kid, "overfill", 5)
        b.add("06_very_dark", str(i), b.sheet(kid, p, degrade=mild), kid, b.expected_from_plan(p), "AUTO_APPROVED")
    # 7. rotated sheets
    for i, rot in enumerate([-4.0, -2.0, 1.5, 3.5, 180.0, 88.0]):
        kid = KEYS[i % 3]
        p = random_plan()
        b.add("07_rotated", f"{rot:+.0f}deg", b.sheet(kid, p, degrade=dict(rotate=rot, noise=3, blur=3, jpeg=90)),
              kid, b.expected_from_plan(p), "AUTO_APPROVED")
    # 8. scan quality / DPI / illumination
    quality = [
        ("100dpi_jpeg60", 100, dict(rotate=0.5, blur=3, jpeg=60)),
        ("150dpi", 150, dict(rotate=-0.8, jpeg=85)),
        ("300dpi", 300, dict(rotate=1.0, blur=3, jpeg=90)),
        ("low_contrast", 200, dict(contrast=0.45, brightness=40, noise=3, jpeg=85)),
        ("dark_scan", 200, dict(brightness=-60, gamma=1.3, jpeg=85)),
        ("shadow_gradient", 200, dict(gradient=0.45, rotate=1.2, jpeg=85)),
        ("scaled_shifted", 200, dict(scale=0.85, shift=(60, -40), rotate=-1.5, jpeg=85)),
        ("phone_perspective", 200, dict(perspective=0.03, rotate=2.0, blur=5, noise=4, jpeg=80)),
        ("blurry", 200, dict(blur=7, jpeg=80)),
    ]
    for i, (name, dpi, deg) in enumerate(quality):
        kid = KEYS[i % 3]
        p = random_plan()
        b.add("08_scan_quality", name, b.sheet(kid, p, dpi=dpi, degrade=deg), kid, b.expected_from_plan(p), "AUTO_APPROVED")
    # 9. noise
    for i, (nz, sp) in enumerate([(10, 0), (18, 300), (25, 800)]):
        kid = KEYS[i % 3]
        p = random_plan()
        b.add("09_noise", f"sigma{nz}_speckle{sp}", b.sheet(kid, p, degrade=dict(noise=nz, speckle=sp, rotate=0.6, jpeg=85)),
              kid, b.expected_from_plan(p), "AUTO_APPROVED")
    # 10. cropped / incorrect images -> FAILED
    kid = KEYS[0]
    p = correct_plan(kid)
    fail_exp = {str(q): None for q in range(1, 11)}
    b.add("10_invalid", "cropped_bottom_missing", b.sheet(kid, p, degrade=dict(crop=(0, 0, 1, 0.42))), kid, fail_exp, "FAILED")
    b.add("10_invalid", "cropped_right_half", b.sheet(kid, p, degrade=dict(crop=(0, 0, 0.55, 1))), kid, fail_exp, "FAILED")
    b.add("10_invalid", "blank_white_page", np.full((2200, 1700), 250, np.uint8), kid, fail_exp, "FAILED")
    other = REPO_ROOT / "samples" / "sample1" / "MobileCamera" / "sheet1.jpg"
    if other.exists():
        b.add("10_invalid", "different_omr_sheet", cv2.imread(str(other), cv2.IMREAD_GRAYSCALE), kid, fail_exp, "FAILED")
    noise_img = (rng.random((2000, 1500)) * 255).astype(np.uint8)
    b.add("10_invalid", "random_noise_image", noise_img, kid, fail_exp, "FAILED")
    # 11. multi-sheet PDF
    import pymupdf

    kid = KEYS[1]
    doc = pymupdf.open()
    pages = []
    for i in range(5):
        p = random_plan() if i != 3 else {**random_plan(), 6: None}
        img = b.sheet(kid, p, degrade=dict(rotate=float(rng.uniform(-2, 2)), noise=4, blur=3))
        ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 88])
        h, w = img.shape
        page = doc.new_page(width=w * 72 / 200, height=h * 72 / 200)
        page.insert_image(page.rect, stream=buf.tobytes())
        pages.append({"page": i + 1, "expected_answers": b.expected_from_plan(p), "expected_status": "AUTO_APPROVED", "note": ""})
    b.n += 1
    fname = f"{b.n:03d}_11_multi_page_pdf_5sheets.pdf"
    doc.save(str(out / fname))
    b.entries.append({"file": fname, "category": "11_multi_page_pdf", "answer_key_id": kid, "pages": pages})
    # 12. tricky marks: ticks, crosses, half fills, stray dots, erased + re-marked
    tricky = [
        ("tick_mark", {3: ("B", "tick")}, {"3": "UNCERTAIN"}, "REVIEW_REQUIRED"),
        ("cross_mark", {7: ("A", "cross")}, {"7": "UNCERTAIN"}, "REVIEW_REQUIRED"),
        ("half_filled", {5: ("C", "half")}, {"5": "UNCERTAIN"}, "REVIEW_REQUIRED"),
        ("stray_dot_on_other_option", {2: [("B", "fill"), ("D", "dot")]}, {"2": "B"}, "AUTO_APPROVED"),
        ("erased_then_remarked", {4: [("A", "erased"), ("C", "fill")]}, {"4": "C"}, "AUTO_APPROVED"),
        ("underfilled_small_mark", {9: ("D", "underfill")}, {"9": "D"}, "AUTO_APPROVED"),
    ]
    for i, (name, change, exp_over, status) in enumerate(tricky):
        for rep in range(3):
            kid = KEYS[(i + rep) % 3]
            p = correct_plan(kid)
            p.update(change)
            exp = b.expected_from_plan(p, exp_over)
            b.add("12_tricky", f"{name}_{rep}", b.sheet(kid, p, degrade=mild), kid, exp, status)

    manifest = {"generator": "omr_app.testing.dataset", "synthetic": True, "entries": b.entries}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    return manifest


# ---------------------------------------------------------------------------- stress / hold-out
ANSWER_STYLES = [("fill", 0.55), ("underfill", 0.12), ("overfill", 0.13), ("light", 0.20)]


def build_stress(out: Path, n=150, seed=777):
    """Random hold-out set: random mark styles, inks and degradations (not used for tuning)."""
    b = Builder(out, seed=seed)
    rng = b.rng
    for i in range(n):
        kid = KEYS[i % 3]
        dpi = int(rng.choice([150, 200, 200, 300]))
        plan, exp = {}, {}
        for q in range(1, 11):
            u = rng.random()
            a = str(rng.choice(OPTIONS))
            if u < 0.80:
                style = str(rng.choice([s for s, _ in ANSWER_STYLES], p=[p for _, p in ANSWER_STYLES]))
                ink = int(rng.uniform(110, 165)) if style == "light" else int(rng.uniform(5, 90))
                plan[q] = (a, style, ink)
                if rng.random() < 0.08:  # stray dot / erased residue on another option
                    plan[q] = [(a, style, ink), (_wrong(a, rng), str(rng.choice(["dot", "erased"])))]
                exp[str(q)] = a
            elif u < 0.87:
                exp[str(q)] = "BLANK"
            elif u < 0.93:
                plan[q] = [(a, "fill"), (_wrong(a, rng), "fill")]
                exp[str(q)] = "MULTIPLE"
            else:
                plan[q] = (a, str(rng.choice(["tick", "cross", "half"])))
                exp[str(q)] = "UNCERTAIN"
        deg = dict(rotate=float(rng.normal(0, 1.8)), noise=float(rng.uniform(0, 14)), blur=int(rng.choice([0, 3, 3, 5])),
                   jpeg=int(rng.uniform(55, 95)), contrast=float(rng.uniform(0.6, 1.1)), brightness=float(rng.uniform(-40, 30)),
                   gradient=float(rng.choice([0, 0, 0.3])), scale=float(rng.uniform(0.85, 1.05)),
                   perspective=float(rng.choice([0, 0, 0.02])), speckle=int(rng.choice([0, 0, 200])))
        if rng.random() < 0.05:
            deg["rotate"] += 180
        img = b.sheet(kid, plan, dpi=dpi, degrade=deg)
        vals = list(exp.values())
        status = "REVIEW_REQUIRED" if any(v in ("MULTIPLE", "UNCERTAIN") for v in vals) or all(v == "BLANK" for v in vals) else "AUTO_APPROVED"
        b.add("stress", f"{dpi}dpi", img, kid, exp, status)
    manifest = {"generator": "omr_app.testing.dataset --stress", "synthetic": True, "seed": seed, "entries": b.entries}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--stress", type=int, default=0, help="generate N random hold-out sheets instead")
    ap.add_argument("--seed", type=int, default=777)
    a = ap.parse_args()
    if a.stress:
        a.out = a.out or str(REPO_ROOT / "tests" / "dataset_stress")
        m = build_stress(Path(a.out), a.stress, a.seed)
    else:
        a.out = a.out or str(REPO_ROOT / "tests" / "dataset")
        m = build(Path(a.out))
    n = sum(len(e["pages"]) for e in m["entries"])
    print(f"wrote {len(m['entries'])} files ({n} sheets) to {a.out}")



if __name__ == "__main__":
    main()
