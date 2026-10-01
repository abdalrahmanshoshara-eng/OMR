"""Command line interface.

    python -m omr_app keys                                   # list answer keys
    python -m omr_app grade sheet.jpg --key institute_2026_business_management
    python -m omr_app grade scans/ --key <id> --out outputs/omr_run1
    python -m omr_app serve                                  # web UI on :8000
"""
import argparse
import json
import logging
import os
import sys
import time
from collections import Counter
from pathlib import Path

from omr_app.imaging import SUPPORTED_EXTS


def _setup_logging(level):
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s", datefmt="%H:%M:%S")
    for noisy in ("matplotlib", "PIL", "multipart", "python_multipart"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def _collect(inputs):
    files = []
    for p in map(Path, inputs):
        if p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.suffix.lower() in SUPPORTED_EXTS)
        elif p.exists():
            files.append(p)
        else:
            print(f"not found: {p}", file=sys.stderr)
    return files


def cmd_keys(args):
    from omr_app.config import load_answer_keys

    for k in load_answer_keys().values():
        ans = " ".join(f"{q}{a}" for q, a in k["answers"].items())
        print(f"{k['id']:<45} {k['exam']} | {k.get('specialization_label', k['specialization'])} | {ans}")


def cmd_grade(args):
    from omr_app.export import summary_rows, to_csv, to_xlsx
    from omr_app.pipeline import Grader

    grader = Grader()
    keys = grader.answer_keys()
    if args.key not in keys:
        sys.exit(f"unknown answer key '{args.key}'. Available: {', '.join(keys)}")
    key = keys[args.key]
    files = _collect(args.inputs)
    if not files:
        sys.exit("no input files")
    out = Path(args.out) if args.out else None
    results = []
    t0 = time.perf_counter()
    for f in files:
        for r in grader.grade_file(f, key, out_dir=out / "images" if out else None):
            results.append(r)
            if out:
                (out / "sheets").mkdir(parents=True, exist_ok=True)
                (out / "sheets" / f"{r['candidate_id']}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    elapsed = time.perf_counter() - t0

    if len(results) == 1 and not args.quiet:
        r = results[0]
        print(json.dumps({"candidate": r["candidate_id"], "answers": r["answers"], "score": r["score"],
                          "status": r["status"], "status_reasons": r["status_reasons"]}, ensure_ascii=False, indent=2))
    cnt = Counter(r["status"] for r in results)
    print(f"\nTotal sheets: {len(results)}")
    print(f"Processed:    {len(results) - cnt['FAILED']}  (auto-approved {cnt['AUTO_APPROVED']})")
    print(f"Needs Review: {cnt['REVIEW_REQUIRED']}")
    print(f"Failed:       {cnt['FAILED']}")
    print(f"Time:         {elapsed:.1f}s ({elapsed / max(1, len(results)) * 1000:.0f} ms/sheet)")
    if out:
        out.mkdir(parents=True, exist_ok=True)
        (out / "results.csv").write_text(to_csv(summary_rows(results)), encoding="utf-8")
        to_xlsx(results, out / "results.xlsx")
        (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        print(f"Results:      {out / 'results.xlsx'} | results.csv | results.json | sheets/*.json | images/")
    for r in results:
        if r["status"] != "AUTO_APPROVED":
            print(f"  [{r['status']}] {r['candidate_id']}: {'; '.join(r['status_reasons'])}")


def cmd_serve(args):
    import uvicorn

    uvicorn.run("omr_app.web.app:app", host=args.host, port=args.port, log_level=args.log_level.lower())


def main(argv=None):
    ap = argparse.ArgumentParser(prog="omr_app", description="Institute OMR grading (OMRChecker based)")
    ap.add_argument("--log-level", default=os.environ.get("OMR_LOG_LEVEL", "INFO"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("keys", help="list answer keys")
    g = sub.add_parser("grade", help="grade images / PDFs / folders")
    g.add_argument("inputs", nargs="+")
    g.add_argument("--key", required=True, help="answer key id (see `keys`)")
    g.add_argument("--out", help="output folder (JSON per sheet, CSV, Excel, overlay images)")
    g.add_argument("--quiet", action="store_true")
    s = sub.add_parser("serve", help="start the web interface")
    s.add_argument("--host", default=os.environ.get("OMR_HOST", "127.0.0.1"))
    s.add_argument("--port", type=int, default=int(os.environ.get("OMR_PORT", 8000)))
    args = ap.parse_args(argv)
    _setup_logging(args.log_level.upper())
    {"keys": cmd_keys, "grade": cmd_grade, "serve": cmd_serve}[args.cmd](args)


if __name__ == "__main__":
    main()
