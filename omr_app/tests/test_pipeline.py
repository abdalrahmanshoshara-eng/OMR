"""End-to-end tests on synthetic sheets rendered from the real blank answer sheet PDF."""
import json

import cv2
import numpy as np
import pytest

from omr_app.config import load_sheet_config
from omr_app.pipeline import Grader
from omr_app.testing.synth import SheetSynth
from pathlib import Path


@pytest.fixture(scope="module")
def grader():
    return Grader()


@pytest.fixture(scope="module")
def synth():
    cfg = load_sheet_config()
    d = Path(cfg["_dir"])
    tpl = json.loads((d / cfg["omr_template"]).read_text())
    return SheetSynth(d / cfg["reference"]["pdf"], tpl, cfg["reference"]["dpi"], dpi=200, seed=42)


@pytest.fixture(scope="module")
def key(grader):
    return grader.answer_keys()["institute_2026_business_management"]


def _sheet(synth, marks, **deg):
    img = synth.make_sheet(marks)
    return synth.degrade(img, **({"rotate": 1.0, "noise": 4, "blur": 3, "jpeg": 85} | deg))


def test_prototype_scenario_all_correct(grader, synth, key):
    marks = [(int(q), a, "fill", 40) for q, a in key["answers"].items()]
    r = grader.grade_image(_sheet(synth, marks), key, source="candidate.jpg")
    assert r["answers"] == key["answers"]
    assert r["score"] == 100
    assert r["status"] == "AUTO_APPROVED"
    # audit data present for every question/option
    assert all(set(q["fills"]) == set("ABCD") for q in r["questions"])


def test_blank_multiple_uncertain(grader, synth, key):
    marks = [(q, "B", "fill", 40) for q in (1, 4, 5, 6, 7, 8, 9, 10)]
    marks += [(2, "A", "fill", 40), (2, "C", "fill", 40)]  # Q2 multiple
    marks += [(10, "D", "cross", 40)]  # Q10: B filled + D crossed -> uncertain
    # Q3 blank
    r = grader.grade_image(_sheet(synth, marks), key, source="mixed.jpg")
    d = r["detected_answers"]
    assert d["2"] == "MULTIPLE" and d["3"] == "BLANK" and d["10"] == "UNCERTAIN"
    assert r["status"] == "REVIEW_REQUIRED"
    assert "Q2: MULTIPLE" in r["status_reasons"]


def test_rotated_upside_down(grader, synth, key):
    marks = [(q, "C", "fill", 40) for q in range(1, 11)]
    r = grader.grade_image(_sheet(synth, marks, rotate=180), key, source="flipped.jpg")
    assert all(v == "C" for v in r["answers"].values())


def test_not_a_sheet_fails(grader, key):
    r = grader.grade_image(np.full((1800, 1300), 245, np.uint8), key, source="white.jpg")
    assert r["status"] == "FAILED" and r["score"] is None


def test_cropped_fails(grader, synth, key):
    marks = [(q, "A", "fill", 40) for q in range(1, 11)]
    r = grader.grade_image(_sheet(synth, marks, crop=(0, 0, 1, 0.4)), key, source="cropped.jpg")
    assert r["status"] == "FAILED"


def test_multi_page_pdf_and_determinism(grader, synth, key, tmp_path):
    import pymupdf

    doc = pymupdf.open()
    answers = []
    for i in range(3):
        ans = "ABCD"[i]
        answers.append(ans)
        img = _sheet(synth, [(q, ans, "fill", 40) for q in range(1, 11)])
        ok, buf = cv2.imencode(".png", img)
        h, w = img.shape
        page = doc.new_page(width=w * 72 / 200, height=h * 72 / 200)
        page.insert_image(page.rect, stream=buf.tobytes())
    pdf = tmp_path / "three.pdf"
    doc.save(str(pdf))
    res = grader.grade_file(pdf, key, out_dir=tmp_path / "out")
    assert [r["page"] for r in res] == [1, 2, 3]
    assert [set(r["answers"].values()) for r in res] == [{a} for a in answers]
    assert (tmp_path / "out" / res[0]["artifacts"]["overlay"]).exists()
    again = grader.grade_file(pdf, key)
    assert [r["questions"][0]["fills"] for r in again] == [r["questions"][0]["fills"] for r in res]
