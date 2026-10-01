"""Run the grader over a dataset manifest and report accuracy metrics.

    python -m omr_app.testing.evaluate --dataset tests/dataset --report tests/reports

Metrics
    * sheets tested / fully correct (status + all 10 answers as expected)
    * detection accuracy (per question, over sheets that were not expected to FAIL)
    * per-question accuracy (Q1..Q10)
    * REVIEW_REQUIRED count, FAILED count
    * false AUTO_APPROVED (approved automatically but an answer is wrong) - must be 0
    * processing time per sheet
"""
import argparse
import json
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path

from omr_app.config import REPO_ROOT
from omr_app.pipeline import Grader


def evaluate(dataset: Path, grader: Grader = None):
    grader = grader or Grader()
    keys = grader.answer_keys()
    manifest = json.loads((dataset / "manifest.json").read_text(encoding="utf-8"))
    rows = []
    for entry in manifest["entries"]:
        key = keys[entry["answer_key_id"]]
        t0 = time.perf_counter()
        results = grader.grade_file(dataset / entry["file"], key)
        elapsed = (time.perf_counter() - t0) * 1000
        for exp in entry["pages"]:
            res = next((r for r in results if r["page"] == exp["page"]), None)
            rows.append(_compare(entry, exp, res, elapsed / max(1, len(results))))
    return summarize(rows), rows


def _compare(entry, exp, res, ms):
    got_status = res["status"] if res else "MISSING"
    got = res.get("detected_answers", {}) if res else {}
    q_ok = {}
    if exp["expected_status"] != "FAILED":
        for q, a in exp["expected_answers"].items():
            q_ok[q] = got.get(q) == a
    mismatches = {q: {"expected": exp["expected_answers"][q], "got": got.get(q)} for q, ok in q_ok.items() if not ok}
    status_ok = got_status == exp["expected_status"]
    return {
        "file": entry["file"], "page": exp["page"], "category": entry["category"],
        "expected_status": exp["expected_status"], "status": got_status, "status_ok": status_ok,
        "answers_ok": all(q_ok.values()) if q_ok else None, "q_ok": q_ok, "mismatches": mismatches,
        "score": res.get("score") if res else None, "ms": round(res.get("processing_ms", ms) if res else ms, 1),
        "error": res.get("error") if res else "no result",
        "fills": {str(qd["q"]): qd["fills"] for qd in res.get("questions", [])} if res else {},
    }


def summarize(rows):
    n = len(rows)
    correct = [r for r in rows if r["status_ok"] and r["answers_ok"] in (True, None)]
    q_total, q_ok = 0, 0
    per_q = defaultdict(lambda: [0, 0])
    for r in rows:
        for q, ok in r["q_ok"].items():
            q_total += 1
            q_ok += ok
            per_q[q][0] += ok
            per_q[q][1] += 1
    false_auto = [r for r in rows if r["status"] == "AUTO_APPROVED" and r["answers_ok"] is False]
    # error taxonomy (per question)
    SPECIAL = ("BLANK", "MULTIPLE", "UNCERTAIN")
    kinds = Counter()
    for r in rows:
        for q, m in r["mismatches"].items():
            e, g = m["expected"], m["got"]
            if e not in SPECIAL and g not in SPECIAL:
                kinds["wrong_letter (critical)"] += 1
            elif e not in SPECIAL and g == "BLANK":
                kinds["answer_read_as_blank (critical)"] += 1
            elif e not in SPECIAL and g in ("MULTIPLE", "UNCERTAIN"):
                kinds["answer_sent_to_review (safe)"] += 1
            elif e in ("MULTIPLE", "UNCERTAIN") and g not in SPECIAL:
                kinds["ambiguous_read_as_answer (risky)"] += 1
            elif e == "BLANK" and g not in SPECIAL:
                kinds["blank_read_as_answer (critical)"] += 1
            else:
                kinds[f"{e}->{g}"] += 1
    times = [r["ms"] for r in rows if r["status"] != "MISSING"]
    by_cat = defaultdict(lambda: [0, 0])
    for r in rows:
        by_cat[r["category"]][1] += 1
        by_cat[r["category"]][0] += int(r in correct)
    return {
        "sheets_tested": n,
        "sheets_fully_correct": len(correct),
        "sheets_with_errors": n - len(correct),
        "status_counts": dict(Counter(r["status"] for r in rows)),
        "review_required": sum(r["status"] == "REVIEW_REQUIRED" for r in rows),
        "failed": sum(r["status"] == "FAILED" for r in rows),
        "false_auto_approved": len(false_auto),
        "error_types": dict(kinds),
        "question_decisions": q_total,
        "question_errors": q_total - q_ok,
        "detection_accuracy": round(q_ok / q_total, 4) if q_total else None,
        "per_question_accuracy": {f"Q{q}": round(v[0] / v[1], 4) for q, v in sorted(per_q.items(), key=lambda kv: int(kv[0]))},
        "per_category": {c: f"{v[0]}/{v[1]}" for c, v in sorted(by_cat.items())},
        "ms_per_sheet_mean": round(statistics.mean(times), 1) if times else None,
        "ms_per_sheet_max": round(max(times), 1) if times else None,
    }


def write_report(summary, rows, report_dir: Path):
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "evaluation.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    lines = ["# OMR evaluation report", "", "> Dataset is SYNTHETIC (generated from the blank sheet PDF). "
             "Real scanned sheets are still required to confirm field accuracy.", "", "## Summary", "", "| metric | value |", "|---|---|"]
    for k, v in summary.items():
        if not isinstance(v, dict):
            lines.append(f"| {k} | {v} |")
    lines += ["", "## Per category", "", "| category | fully correct |", "|---|---|"]
    lines += [f"| {c} | {v} |" for c, v in summary["per_category"].items()]
    lines += ["", "## Per question accuracy", "", "| question | accuracy |", "|---|---|"]
    lines += [f"| {q} | {v:.2%} |" for q, v in summary["per_question_accuracy"].items()]
    lines += ["", "## Sheets", "", "| file | page | expected | got | answers ok | score | ms | notes |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        notes = "; ".join(f"Q{q}: exp {m['expected']} got {m['got']}" for q, m in r["mismatches"].items())
        if r["status"] == "FAILED":
            notes = (notes + " " if notes else "") + f"({r['error']})"
        lines.append(f"| {r['file']} | {r['page']} | {r['expected_status']} | {r['status']} | {r['answers_ok']} | {r['score']} | {r['ms']} | {notes} |")
    (report_dir / "evaluation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    import logging

    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=str(REPO_ROOT / "tests" / "dataset"))
    ap.add_argument("--report", default=str(REPO_ROOT / "tests" / "reports"))
    ap.add_argument("--log-level", default="WARNING")
    a = ap.parse_args()
    logging.basicConfig(level=a.log_level, format="%(levelname)s %(name)s: %(message)s")
    summary, rows = evaluate(Path(a.dataset))
    write_report(summary, rows, Path(a.report))
    print(json.dumps(summary, indent=1))
    for r in rows:
        if not (r["status_ok"] and r["answers_ok"] in (True, None)):
            print("MISMATCH", r["file"], r["page"], r["expected_status"], "->", r["status"], r["mismatches"], r["error"] or "")


if __name__ == "__main__":
    main()
