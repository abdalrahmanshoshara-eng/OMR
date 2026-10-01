"""Excel / PDF report export of grading results (plus the full CSV summary used by the CLI)."""
import csv
import html
import io

# columns of the Excel report: (header, value getter)
REPORT_COLUMNS = [
    ("الاختصاص", lambda r, lbl: lbl(r)),
    ("رقم الصفحة في ملف PDF", lambda r, lbl: r.get("page")),
    ("الاسم", lambda r, lbl: _name(r)),
    ("الإجابات الصحيحة", lambda r, lbl: r.get("correct_count")),
    ("الإجابات الخاطئة", lambda r, lbl: _wrong(r)),
    ("العلامة", lambda r, lbl: r.get("score")),
    ("العلامة القصوى", lambda r, lbl: r.get("max_score")),
    ("المراجِع", lambda r, lbl: r.get("reviewed_by") or ""),
]


def _name(r):
    return r.get("candidate_name") or r.get("candidate_id") or ""


def _wrong(r):
    """Every question that did not earn points (wrong, blank or unresolved)."""
    if r.get("correct_count") is None:
        return None
    return (r.get("wrong_count") or 0) + (r.get("blank_count") or 0)


def _label_fn(spec_labels):
    spec_labels = spec_labels or {}
    return lambda r: spec_labels.get(r.get("answer_key_id")) or r.get("specialization") or ""


def score_100(r):
    """Score scaled to 100 (the key's total may differ from 100)."""
    if r.get("score") is None or not r.get("max_score"):
        return None
    return round(100 * r["score"] / r["max_score"], 2)


def summary_rows(results):
    rows = []
    for r in results:
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
        for q in sorted(answers, key=int):
            row[f"Q{q}"] = answers[q]
        row["status_reasons"] = "; ".join(r.get("status_reasons") or [])
        row["reviewed_by"] = r.get("reviewed_by") or ""
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


def to_xlsx(results, path_or_buffer, title="OMR Results", spec_labels=None):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    lbl = _label_fn(spec_labels)
    wb = Workbook()
    ws = wb.active
    ws.title = "النتائج"
    ws.sheet_view.rightToLeft = True
    ws.append([h for h, _ in REPORT_COLUMNS])
    for c in ws[1]:
        c.font, c.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3A5F")
        c.alignment = Alignment(horizontal="center")
    for r in results:
        ws.append([get(r, lbl) for _, get in REPORT_COLUMNS])
    for i, (h, get) in enumerate(REPORT_COLUMNS, 1):
        width = max([len(h)] + [len(str(get(r, lbl) or "")) for r in results[:200]]) + 4
        ws.column_dimensions[get_column_letter(i)].width = min(width, 50)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    wb.save(path_or_buffer)


def to_pdf(results, title="OMR Results", spec_labels=None) -> bytes:
    """A4 RTL table: name, specialization, score out of 100 (multi-page)."""
    import pymupdf

    lbl = _label_fn(spec_labels)
    e = html.escape
    cell = "border:1px solid #555;padding:4px 6px;"
    rows = "".join(
        f'<tr><td style="{cell}text-align:center">{i}</td><td style="{cell}">{e(_name(r))}</td>'
        f'<td style="{cell}">{e(lbl(r))}</td>'
        f'<td style="{cell}text-align:center">{"—" if score_100(r) is None else f"{score_100(r):g}"}</td></tr>'
        for i, r in enumerate(results, 1)
    )
    head = f"background-color:#1f3a5f;color:#fff;{cell}"
    body = (
        f'<div dir="rtl" style="font-size:11pt">'
        f'<h2 style="text-align:center">{e(title)}</h2>'
        f'<table style="border-collapse:collapse;width:100%">'
        f'<tr><th style="{head}width:8%">#</th><th style="{head}width:42%">الاسم</th>'
        f'<th style="{head}width:35%">الاختصاص</th><th style="{head}width:15%">العلامة / 100</th></tr>'
        f"{rows}</table></div>"
    )
    story = pymupdf.Story(html=body)
    buf = io.BytesIO()
    writer = pymupdf.DocumentWriter(buf)
    page_rect = pymupdf.paper_rect("a4")
    where = page_rect + (36, 36, -36, -36)
    more = True
    while more:
        dev = writer.begin_page(page_rect)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    writer.close()
    return buf.getvalue()
