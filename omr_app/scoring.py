"""Answer-key comparison, scoring and sheet status. Independent of image processing."""
from omr_app.detection import BLANK, MULTIPLE, UNCERTAIN

AUTO_APPROVED = "AUTO_APPROVED"
REVIEW_REQUIRED = "REVIEW_REQUIRED"
FAILED = "FAILED"
MANUALLY_REVIEWED = "MANUALLY_REVIEWED"
STATUSES = (AUTO_APPROVED, REVIEW_REQUIRED, FAILED, MANUALLY_REVIEWED)


def question_points(scoring: dict, q: str) -> float:
    per_q = scoring.get("question_scores") or {}
    return float(per_q.get(q, scoring.get("question_score", 0)))


def score_questions(questions: list, answer_key: dict) -> dict:
    """Fill expected/final/correct/points in each question dict (in place) and total them.

    final answer = manual override if present, else the detected answer.
    """
    scoring = answer_key["scoring"]
    total, correct, wrong, blank, unresolved = 0.0, 0, 0, 0, 0
    for qd in questions:
        q = str(qd["q"])
        expected = answer_key["answers"].get(q)
        final = qd.get("override") or qd["detected"]
        qd["expected"] = expected
        qd["final"] = final
        qd["correct"] = final == expected
        if expected is None:  # printed question not in this answer key: not graded
            qd["points"] = 0.0
            continue
        if qd["correct"]:
            pts = question_points(scoring, q)
            correct += 1
        elif final == BLANK:
            pts = float(scoring.get("blank_score", 0))
            blank += 1
        else:
            pts = float(scoring.get("wrong_score", 0))
            wrong += 1
            if final in (MULTIPLE, UNCERTAIN):
                unresolved += 1
        qd["points"] = pts
        total += pts
    total = max(0.0, min(total, float(scoring["total_score"])))
    return {
        "score": round(total, 2),
        "max_score": float(scoring["total_score"]),
        "correct_count": correct,
        "wrong_count": wrong,
        "blank_count": blank,
        "unresolved_count": unresolved,
    }


def sheet_status(questions: list, review_cfg: dict, low_alignment: bool):
    """AUTO_APPROVED only when every question has a clear decision."""
    reasons = []
    for qd in questions:
        final = qd.get("override") or qd["detected"]
        if final in (MULTIPLE, UNCERTAIN):
            reasons.append(f"Q{qd['q']}: {final}")
        elif final == BLANK and review_cfg.get("review_on_blank") and not qd.get("override"):
            reasons.append(f"Q{qd['q']}: BLANK")
    if questions and review_cfg.get("review_on_all_blank", True) and all(
        (qd.get("override") or qd["detected"]) == BLANK for qd in questions
    ):
        reasons.append("all questions blank")
    if low_alignment and review_cfg.get("review_on_low_alignment", True):
        reasons.append("low alignment confidence")
    return (REVIEW_REQUIRED if reasons else AUTO_APPROVED), reasons
