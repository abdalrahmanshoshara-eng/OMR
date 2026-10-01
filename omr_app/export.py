"""CSV / Excel / JSON export of grading results (with full per-question audit data)."""
import csv
import io
import json

OPTIONS = ["A", "B", "C", "D"]


def summary_rows(results):
    rows = []
    for r in results:
        nq = len(r.get("questions") or []) or 10
        row = {
            "candidate_id": r.get("candidate_id"),
            "candidate_name": r.get("candidate_name") or "",
            "source_file": r.get("source_file"),
            "page": r.get("page"),
            "exam": r.get("exam"),
            "specialization": r.get("specialization"),
            "answer_key_id": r.get("answer_key_id"),
            "status": r.get("status"),
            "score": r.get("score"),
            "max_score": r.get("max_score"),
            "correct": r.get("correct_count"),
            "wrong": r.get("wrong_count"),
            "blank": r.get("blank_count"),
            "unresolved": r.get("unresolved_count"),
        }
        answers = r.get("answers") or {}
        detected = r.get("detected_answers") or {}
        for q in range(1, nq + 1):
            row[f"Q{q}"] = answers.get(str(q), "")
        for q in range(1, nq + 1):
            if detected.get(str(q)) != answers.get(str(q)):
                row.setdefault("manual_changes", "")
                row["manual_changes"] += f"Q{q}:{detected.get(str(q))}->{answers.get(str(q))} "
        row["manual_changes"] = row.get("manual_changes", "").strip()
        row["status_reasons"] = "; ".join(r.get("status_reasons") or [])
        row["reviewed_by"] = r.get("reviewed_by") or ""
        row["config_fingerprint"] = r.get("config_fingerprint")
        rows.append(row)
    return rows


def detail_rows(results):
    """One row per question: fill ratios per option, detected, expected, final, override."""
    rows = []
    for r in results:
        for qd in r.get("questions") or []:
            row = {"candidate_id": r.get("candidate_id"), "source_file": r.get("source_file"), "page": r.get("page"), "question": qd["q"]}
            for o in OPTIONS:
                if o in qd["fills"]:
                    row[f"fill_{o}"] = qd["fills"][o]
            for o in OPTIONS:
                if o in qd.get("hole", {}):
                    row[f"inside_O_{o}"] = qd["hole"][o]
            row.update({
                "detected": qd["detected"], "reason": qd.get("reason"), "override": qd.get("override") or "",
                "final": qd.get("final"), "expected": qd.get("expected"), "correct": qd.get("correct"), "points": qd.get("points"),
            })
            rows.append(row)
    return rows


def to_csv(rows) -> str:
    if not rows:
        return ""
    keys = list(dict.fromkeys(k for r in rows for k in r))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=keys)
    w.writeheader()
    w.writerows(rows)
    return "﻿" + buf.getvalue()  # BOM so Excel opens UTF-8 (Arabic) correctly


def to_xlsx(results, path_or_buffer, title="OMR Results"):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    fills = {
        "AUTO_APPROVED": PatternFill("solid", fgColor="D8F3DC"),
        "MANUALLY_REVIEWED": PatternFill("solid", fgColor="D0E7FF"),
        "REVIEW_REQUIRED": PatternFill("solid", fgColor="FFE8B3"),
        "FAILED": PatternFill("solid", fgColor="F8D0D0"),
    }
    special = PatternFill("solid", fgColor="FFE8B3")
    wrong = Font(color="B42318")
    head = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor="1F3A5F")

    wb = Workbook()
    ws = wb.active
    ws.title = "Results"
    srows = summary_rows(results)

    def write(ws, rows):
        if not rows:
            ws.append(["no data"])
            return []
        keys = list(dict.fromkeys(k for r in rows for k in r))
        ws.append(keys)
        for c in ws[1]:
            c.font, c.fill, c.alignment = head, head_fill, Alignment(horizontal="center")
        for r in rows:
            ws.append([r.get(k) for k in keys])
        for i, k in enumerate(keys, 1):
            width = max(len(str(k)), *(len(str(r.get(k, ""))) for r in rows[:200])) + 2
            ws.column_dimensions[get_column_letter(i)].width = min(width, 50)
        ws.freeze_panes = "B2"
        ws.auto_filter.ref = ws.dimensions
        return keys

    keys = write(ws, srows)
    if srows:
        si = keys.index("status") + 1
        for row_idx, (res, row) in enumerate(zip(results, srows), start=2):
            ws.cell(row_idx, si).fill = fills.get(row["status"], PatternFill())
            expected = {str(q["q"]): q.get("expected") for q in res.get("questions") or []}
            for q in range(1, 11):
                k = f"Q{q}"
                if k in keys:
                    c = ws.cell(row_idx, keys.index(k) + 1)
                    if c.value in ("BLANK", "MULTIPLE", "UNCERTAIN"):
                        c.fill = special
                    elif expected.get(str(q)) and c.value != expected.get(str(q)):
                        c.font = wrong

    ws2 = wb.create_sheet("Question details")
    write(ws2, detail_rows(results))

    ws3 = wb.create_sheet("Summary")
    from collections import Counter

    cnt = Counter(r.get("status") for r in results)
    scores = [r["score"] for r in results if r.get("score") is not None]
    ws3.append([title])
    ws3["A1"].font = Font(bold=True, size=14)
    for k, v in [("Total sheets", len(results)), *[(s, cnt.get(s, 0)) for s in fills],
                 ("Average score", round(sum(scores) / len(scores), 2) if scores else "-")]:
        ws3.append([k, v])
    ws3.column_dimensions["A"].width = 28
    wb.save(path_or_buffer)


def to_json(results) -> str:
    return json.dumps(results, ensure_ascii=False, indent=1, default=str)
