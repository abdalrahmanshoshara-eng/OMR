"""Unit tests: classification rules, scoring, status and answer-key config (no images)."""
import pytest

from omr_app.config import ConfigError, load_answer_keys, load_thresholds, validate_answer_key
from omr_app.detection import BLANK, MULTIPLE, UNCERTAIN, classify_question
from omr_app.scoring import AUTO_APPROVED, REVIEW_REQUIRED, score_questions, sheet_status

TH = load_thresholds()["classification"]


def b(fill, hole=None, shape="none", hd=0.0):
    return {"fill": fill, "hole": fill if hole is None else hole, "shape": shape, "hole_darkness": hd}


def cls(**opts):
    return classify_question({o: opts.get(o, b(0.0)) for o in "ABCD"}, TH)[0]


def test_single_clear_mark():
    assert cls(B=b(0.82, 1.0)) == "B"


def test_blank():
    assert cls(A=b(0.05), C=b(0.03)) == BLANK


def test_multiple():
    assert cls(A=b(0.9, 1.0), B=b(0.85, 1.0)) == MULTIPLE


def test_partial_is_uncertain():
    assert cls(C=b(0.33)) == UNCERTAIN


def test_mark_plus_partial_is_uncertain():
    assert cls(A=b(0.9, 1.0), D=b(0.3)) == UNCERTAIN


def test_tick_or_cross_never_accepted():
    assert cls(B=b(0.7, 1.0, shape="strokes")) == UNCERTAIN


def test_hollow_mark_not_accepted():
    assert cls(B=b(0.6, hole=0.5)) == UNCERTAIN


def test_faint_mark_is_uncertain_not_blank():
    assert cls(B=b(0.05, hd=0.2)) == UNCERTAIN


def test_faint_residue_next_to_clear_mark_ignored():
    assert cls(A=b(0.03, hd=0.2), C=b(0.95, 1.0)) == "C"


def test_ambiguity_gap(monkeypatch):
    th = {**TH, "ambiguity_gap": 0.9}
    assert classify_question({"A": b(0.8, 1.0), "B": b(0.0), "C": b(0.0), "D": b(0.0)}, th)[0] == UNCERTAIN


# ------------------------------------------------------------------ keys / scoring
def test_answer_keys_match_marking_scheme():
    keys = load_answer_keys()
    got = {k["specialization"]: "".join(k["answers"][str(i)] for i in range(1, 11)) for k in keys.values()}
    assert got == {
        # سلم تصحيح المعاهد
        "business_management": "BCABBBBBBB",
        "commercial_banking": "BBAAABBBCB",
        "applied_statistics": "BBABBAAABB",
        # سلم تصحيح الهندسات
        "mechanical_engineering": "BBCCCBBBBB",
        "electrical_engineering": "ADBABBBBBB",
        "civil_engineering": "CCABBBBBBB",
        "informatics_engineering": "BABBBBBBBB",
        # سلم تصحيح رياضيات + اقتصاد
        "commerce_economics": "BBBABBBBBB",
        "mathematics": "BBBBBBBBBA",
    }
    for k in keys.values():
        assert k["scoring"]["total_score"] == 100 and k["scoring"]["question_score"] == 10


def test_invalid_answer_key_rejected():
    with pytest.raises(ConfigError):
        validate_answer_key({"id": "x_bad", "exam": "e", "specialization": "s", "answers": {"1": "E"}}, 10, list("ABCD"))


def _qs(finals):
    return [{"q": i + 1, "detected": v, "override": None} for i, v in enumerate(finals)]


def test_score_and_status():
    key = load_answer_keys()["institute_2026_business_management"]
    qs = _qs(list("BCABBBBBBB"))
    s = score_questions(qs, key)
    assert s["score"] == 100 and s["correct_count"] == 10
    assert sheet_status(qs, {"review_on_blank": False}, False)[0] == AUTO_APPROVED
    qs = _qs(list("BCABBBBBB") + [MULTIPLE])
    s = score_questions(qs, key)
    assert s["score"] == 90
    assert sheet_status(qs, {"review_on_blank": False}, False)[0] == REVIEW_REQUIRED
    qs[9]["override"] = "B"  # manual resolution
    assert score_questions(qs, key)["score"] == 100
    assert sheet_status(qs, {"review_on_blank": False}, False)[0] == AUTO_APPROVED


def test_all_blank_sheet_goes_to_review():
    qs = _qs([BLANK] * 10)
    assert sheet_status(qs, {"review_on_blank": False, "review_on_all_blank": True}, False)[0] == REVIEW_REQUIRED


def test_blank_not_allowed_sends_sheet_to_review_until_a_letter_is_chosen():
    cfg = {"review_on_blank": False, "blank_not_allowed": True}
    qs = _qs(["A"] * 9 + [BLANK])
    status, reasons = sheet_status(qs, cfg, False)
    assert status == REVIEW_REQUIRED and reasons == ["Q10: BLANK"]
    qs[-1]["override"] = "C"  # reviewer chose a letter
    assert sheet_status(qs, cfg, False)[0] == AUTO_APPROVED
    qs[-1]["override"] = BLANK  # a blank entered by hand is still not accepted
    assert sheet_status(qs, cfg, False)[0] == REVIEW_REQUIRED


def test_blank_allowed_by_default():
    assert sheet_status(_qs(["A"] * 9 + [BLANK]), {"review_on_blank": False}, False)[0] == AUTO_APPROVED


def test_answer_key_any_question_count():
    ans = {str(i): "A" for i in range(1, 16)}
    k = validate_answer_key({"id": "x_15", "exam": "e", "specialization": "s", "answers": ans}, 10, list("ABCD"))
    assert len(k["answers"]) == 15 and k["scoring"]["question_score"] == pytest.approx(100 / 15)
    with pytest.raises(ConfigError):  # gap in numbering
        validate_answer_key({"id": "x_gap", "exam": "e", "specialization": "s", "answers": {"1": "A", "3": "B"}}, 10, list("ABCD"))
    # sheet questions missing from a shorter key are not graded
    short = validate_answer_key({"id": "x_5", "exam": "e", "specialization": "s", "answers": {str(i): "B" for i in range(1, 6)}}, 10, list("ABCD"))
    s = score_questions(_qs(list("BBBBBCCCCC")), short)
    assert s["score"] == 100 and s["correct_count"] == 5 and s["wrong_count"] == 0
