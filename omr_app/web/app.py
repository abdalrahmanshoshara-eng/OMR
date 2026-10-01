"""Web interface / REST API for batch grading and manual review.

Run:  python -m omr_app serve        (or: uvicorn omr_app.web.app:app)
Data: $OMR_DATA_DIR (default <repo>/data): SQLite DB, uploads, generated images.
"""
import io
import json
import logging
import os
import queue
import re
import shutil
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from omr_app import __version__
from omr_app.config import REPO_ROOT, ConfigError, config_dir, save_answer_key
from omr_app.detection import SPECIAL_VALUES
from omr_app.export import detail_rows, summary_rows, to_csv, to_json, to_xlsx
from omr_app.imaging import SUPPORTED_EXTS
from omr_app.pipeline import Grader
from omr_app.scoring import FAILED, MANUALLY_REVIEWED, REVIEW_REQUIRED
from omr_app.web.store import Store

log = logging.getLogger("omr_app.web")
if not logging.getLogger().handlers:
    logging.basicConfig(level=os.environ.get("OMR_LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")

DATA_DIR = Path(os.environ.get("OMR_DATA_DIR", REPO_ROOT / "data"))
STATIC_DIR = Path(__file__).parent / "static"
MAX_UPLOAD_MB = int(os.environ.get("OMR_MAX_UPLOAD_MB", 200))

store = Store(DATA_DIR / "omr.db")
grader = Grader()
grader_lock = threading.Lock()
jobs: "queue.Queue[int]" = queue.Queue()



@asynccontextmanager
async def lifespan(_app):
    threading.Thread(target=_worker, daemon=True, name="omr-worker").start()
    for b in store.q("SELECT id FROM batches WHERE state IN ('queued','processing') ORDER BY id"):
        jobs.put(b["id"])  # resume unfinished work after a restart
    yield


app = FastAPI(title="OMR Grader", version=__version__, lifespan=lifespan)


# --------------------------------------------------------------------------- helpers
def _keys():
    with grader_lock:
        return grader.answer_keys()


def _key(key_id):
    keys = _keys()
    if key_id not in keys:
        raise HTTPException(400, f"unknown answer key '{key_id}'")
    return keys[key_id]


def _batch_dir(batch_id):
    return DATA_DIR / "batches" / str(batch_id)


def _safe_name(name):
    name = Path(name).name
    return re.sub(r"[^\w.\- ]", "_", name, flags=re.UNICODE)[:150] or "file"


# --------------------------------------------------------------------------- worker
def _process_batch(batch_id):
    b = store.batch(batch_id)
    if not b:
        return
    store.x("UPDATE batches SET state='processing' WHERE id=?", (batch_id,))
    try:
        key = _key(b["answer_key_id"])
        uploads = store.q("SELECT * FROM uploads WHERE batch_id=? AND state!='done' ORDER BY idx", (batch_id,))
        for up in uploads:
            store.x("DELETE FROM sheets WHERE upload_id=?", (up["id"],))  # idempotent resume
            img_dir = _batch_dir(batch_id) / "images" / str(up["idx"])
            stem = Path(up["original_name"]).stem
            with grader_lock:
                results = grader.grade_file(Path(up["stored_path"]), key, out_dir=img_dir, candidate_id=None)
            for r in results:
                r["source_file"] = up["original_name"]
                r["candidate_id"] = stem if len(results) == 1 else f"{stem}_p{r['page']}"
                sid = store.insert_sheet(batch_id, up["id"], r, img_dir)
                store.audit(sid, "processed", {"status": r["status"], "score": r.get("score"),
                                               "detected": r.get("detected_answers"), "reasons": r.get("status_reasons")})
            store.x("UPDATE uploads SET state='done' WHERE id=?", (up["id"],))
            store.x("UPDATE batches SET processed_files=processed_files+1 WHERE id=?", (batch_id,))
        store.x("UPDATE batches SET state='done' WHERE id=?", (batch_id,))
        b = store.batch(batch_id)
        log.info("batch %s done: %s", batch_id, b["counts"])
    except Exception as e:  # keep the worker alive
        log.exception("batch %s failed", batch_id)
        store.x("UPDATE batches SET state='error', error=? WHERE id=?", (str(e), batch_id))


def _worker():
    while True:
        bid = jobs.get()
        try:
            _process_batch(bid)
        finally:
            jobs.task_done()


# --------------------------------------------------------------------------- meta / config
@app.get("/api/meta")
def meta():
    raw = json.loads((config_dir() / "thresholds.json").read_text(encoding="utf-8"))
    L = grader.layout
    return {
        "version": __version__,
        "sheet_id": L.sheet_id,
        "questions": L.num_questions,
        "options": L.options,
        "special_values": list(SPECIAL_VALUES),
        "thresholds": {k: v for k, v in raw.items() if k != "_doc"},
        "threshold_docs": raw.get("_doc", {}),
        "config_fingerprint": grader.fingerprint,
        "config_dir": str(config_dir()),
        "supported_ext": sorted(SUPPORTED_EXTS),
        "queue": jobs.qsize(),
    }


@app.get("/api/keys")
def list_keys():
    return [{k: v for k, v in key.items() if not k.startswith("_")} for key in _keys().values()]


class KeyIn(BaseModel):
    id: str
    exam: str
    specialization: str
    specialization_label: Optional[str] = None
    specialization_label_ar: Optional[str] = None
    answers: Dict[str, str]
    scoring: Optional[dict] = None


@app.post("/api/keys")
def upsert_key(k: KeyIn):
    data = {kk: v for kk, v in k.dict().items() if v is not None}
    try:
        with grader_lock:
            saved = save_answer_key(data)
    except ConfigError as e:
        raise HTTPException(400, str(e))
    log.info("answer key saved: %s", saved["id"])
    return saved


# --------------------------------------------------------------------------- batches
@app.get("/api/batches")
def list_batches():
    return store.batches()


@app.post("/api/batches")
async def create_batch(answer_key_id: str = Form(...), name: str = Form(""), files: List[UploadFile] = File(...)):
    _key(answer_key_id)
    files = [f for f in files if f.filename]
    if not files:
        raise HTTPException(400, "no files uploaded")
    bad = [f.filename for f in files if Path(f.filename).suffix.lower() not in SUPPORTED_EXTS]
    if bad:
        raise HTTPException(400, f"unsupported file type: {', '.join(bad)}")
    name = name.strip() or time.strftime("Batch %Y-%m-%d %H:%M")
    bid = store.create_batch(name, answer_key_id, len(files))
    up_dir = _batch_dir(bid) / "uploads"
    up_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    for i, f in enumerate(files, 1):
        dest = up_dir / f"{i:04d}_{_safe_name(f.filename)}"
        with open(dest, "wb") as out:
            while chunk := await f.read(1 << 20):
                total += len(chunk)
                if total > MAX_UPLOAD_MB * (1 << 20):
                    raise HTTPException(413, f"upload larger than {MAX_UPLOAD_MB} MB")
                out.write(chunk)
        store.add_upload(bid, i, Path(f.filename).name, dest)
    log.info("batch %s created: %d files, key %s", bid, len(files), answer_key_id)
    jobs.put(bid)
    return store.batch(bid)


@app.get("/api/batches/{bid}")
def get_batch(bid: int):
    b = store.batch(bid)
    if not b:
        raise HTTPException(404, "batch not found")
    return b


@app.delete("/api/batches/{bid}")
def delete_batch(bid: int):
    b = store.batch(bid)
    if not b:
        raise HTTPException(404, "batch not found")
    if b["state"] in ("queued", "processing"):
        raise HTTPException(409, "batch is still processing")
    store.x("DELETE FROM batches WHERE id=?", (bid,))
    shutil.rmtree(_batch_dir(bid), ignore_errors=True)
    return {"deleted": bid}


@app.get("/api/batches/{bid}/sheets")
def batch_sheets(bid: int, status: Optional[str] = None):
    return store.sheets(bid, status)


class RekeyIn(BaseModel):
    answer_key_id: str
    actor: Optional[str] = None


@app.post("/api/batches/{bid}/answer-key")
def rekey_batch(bid: int, body: RekeyIn):
    """Change the answer key (specialization) of a whole batch and re-score every sheet."""
    key = _key(body.answer_key_id)
    store.x("UPDATE batches SET answer_key_id=? WHERE id=?", (key["id"], bid))
    for s in store.sheets(bid, with_result=True):
        r = s["result"]
        old = r.get("answer_key_id")
        if r["status"] != FAILED or r.get("questions"):
            grader.finalize(r, key)
        else:
            r["answer_key_id"], r["exam"], r["specialization"] = key["id"], key["exam"], key["specialization"]
        store.update_sheet(s["id"], r)
        store.audit(s["id"], "answer_key_changed", {"from": old, "to": key["id"], "score": r.get("score")}, body.actor)
    return store.batch(bid)


def _export_results(bid):
    return [s["result"] | {"reviewed_by": s["result"].get("reviewed_by")} for s in store.sheets(bid, with_result=True)]


@app.get("/api/batches/{bid}/export.{fmt}")
def export_batch(bid: int, fmt: str, details: bool = False):
    b = store.batch(bid)
    if not b:
        raise HTTPException(404, "batch not found")
    results = _export_results(bid)
    base = re.sub(r"[^\w\-]+", "_", b["name"], flags=re.UNICODE).strip("_") or f"batch_{bid}"
    if fmt == "csv":
        body = to_csv(detail_rows(results) if details else summary_rows(results))
        fn = f"{base}{'_details' if details else ''}.csv"
        return Response(body.encode("utf-8"), media_type="text/csv; charset=utf-8", headers=_dl(fn))
    if fmt == "xlsx":
        buf = io.BytesIO()
        to_xlsx(results, buf, title=b["name"])
        return Response(buf.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=_dl(f"{base}.xlsx"))
    if fmt == "json":
        return Response(to_json(results).encode("utf-8"), media_type="application/json", headers=_dl(f"{base}.json"))
    raise HTTPException(400, "format must be csv, xlsx or json")


def _dl(filename):
    from urllib.parse import quote

    return {"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"}


# --------------------------------------------------------------------------- sheets / review
@app.get("/api/sheets/{sid}")
def get_sheet(sid: int):
    s = store.sheet(sid)
    if not s:
        raise HTTPException(404, "sheet not found")
    s["audit"] = store.audit_log(sid)
    ids = [r["id"] for r in store.q("SELECT id FROM sheets WHERE batch_id=? ORDER BY id", (s["batch_id"],))]
    queue_ids = [r["id"] for r in store.q("SELECT id FROM sheets WHERE batch_id=? AND status=? ORDER BY id", (s["batch_id"], REVIEW_REQUIRED))]
    i = ids.index(sid)
    s["nav"] = {
        "prev": ids[i - 1] if i > 0 else None,
        "next": ids[i + 1] if i + 1 < len(ids) else None,
        "next_review": next((q for q in queue_ids if q > sid), queue_ids[0] if queue_ids and queue_ids[0] != sid else None),
        "position": i + 1, "total": len(ids), "review_left": len(queue_ids),
    }
    s["batch"] = store.q("SELECT id, name, answer_key_id FROM batches WHERE id=?", (s["batch_id"],), one=True)
    return s


class ReviewIn(BaseModel):
    candidate_id: Optional[str] = None
    candidate_name: Optional[str] = None
    answer_key_id: Optional[str] = None
    overrides: Optional[Dict[str, Optional[str]]] = None  # {"5": "B"} ; null/"" removes the override
    approve: bool = False
    reopen: bool = False
    actor: Optional[str] = None
    note: Optional[str] = None


@app.patch("/api/sheets/{sid}")
def review_sheet(sid: int, body: ReviewIn):
    s = store.sheet(sid)
    if not s:
        raise HTTPException(404, "sheet not found")
    r = s["result"]
    changes = {}
    for fld in ("candidate_id", "candidate_name"):
        v = getattr(body, fld)
        if v is not None and v.strip() != (r.get(fld) or ""):
            changes[fld] = {"from": r.get(fld), "to": v.strip()}
            r[fld] = v.strip()
    key = _key(body.answer_key_id or r.get("answer_key_id"))
    if key["id"] != r.get("answer_key_id"):
        changes["answer_key_id"] = {"from": r.get("answer_key_id"), "to": key["id"]}
    allowed = set(grader.layout.options) | {"BLANK"}
    if body.overrides:
        if not r.get("questions"):
            raise HTTPException(400, "this sheet could not be read (FAILED); answers cannot be overridden")
        by_q = {str(qd["q"]): qd for qd in r["questions"]}
        for q, v in body.overrides.items():
            if q not in by_q:
                raise HTTPException(400, f"unknown question {q}")
            v = (v or "").strip().upper() or None
            if v is not None and v not in allowed:
                raise HTTPException(400, f"invalid answer '{v}' for Q{q}")
            if v == by_q[q]["detected"]:
                v = None  # same as detection -> no override
            if v != by_q[q].get("override"):
                changes[f"Q{q}"] = {"from": by_q[q].get("override") or by_q[q]["detected"], "to": v or by_q[q]["detected"],
                                    "detected": by_q[q]["detected"]}
                by_q[q]["override"] = v
    if body.reopen:
        r["reviewed"] = False
        changes["reopened"] = True
    if r.get("questions"):
        r["reviewed"] = r.get("reviewed", False) and not body.reopen
        grader.finalize(r, key)
        if body.approve:
            unresolved = [f"Q{qd['q']}" for qd in r["questions"] if qd["final"] in ("MULTIPLE", "UNCERTAIN")]
            if unresolved:
                raise HTTPException(400, f"resolve {', '.join(unresolved)} (choose A-D or BLANK) before approving")
            r["reviewed"] = True
            r["reviewed_by"] = body.actor
            r["reviewed_at"] = time.time()
            grader.finalize(r, key)
            changes["approved"] = True
    else:
        r["answer_key_id"], r["exam"], r["specialization"] = key["id"], key["exam"], key["specialization"]
    if body.note:
        changes["note"] = body.note
    store.update_sheet(sid, r)
    if changes:
        store.audit(sid, "review", {**changes, "score": r.get("score"), "status": r["status"]}, body.actor)
    return get_sheet(sid)


@app.post("/api/sheets/{sid}/reprocess")
def reprocess_sheet(sid: int, actor: Optional[str] = None):
    """Re-run detection with the current configuration (manual overrides are kept)."""
    s = store.sheet(sid)
    if not s:
        raise HTTPException(404, "sheet not found")
    up = store.q("SELECT * FROM uploads WHERE id=?", (s["upload_id"],), one=True)
    old = s["result"]
    key = _key(old.get("answer_key_id"))
    with grader_lock:
        grader.reload()
        results = grader.grade_file(Path(up["stored_path"]), key, out_dir=Path(s["image_dir"]))
    r = next((x for x in results if x["page"] == s["page"]), None)
    if r is None:
        raise HTTPException(500, "page not found on re-processing")
    r["source_file"], r["candidate_id"], r["candidate_name"] = old["source_file"], old.get("candidate_id"), old.get("candidate_name")
    prev = {str(q["q"]): q.get("override") for q in old.get("questions", [])}
    for qd in r.get("questions", []):
        qd["override"] = prev.get(str(qd["q"]))
    if r.get("questions"):
        grader.finalize(r, key)
    store.update_sheet(sid, r)
    store.audit(sid, "reprocessed", {"status": r["status"], "score": r.get("score"), "config": r.get("config_fingerprint")}, actor)
    return get_sheet(sid)


@app.get("/api/sheets/{sid}/image/{kind}")
def sheet_image(sid: int, kind: str):
    s = store.sheet(sid)
    if not s:
        raise HTTPException(404, "sheet not found")
    if kind == "original":
        up = store.q("SELECT * FROM uploads WHERE id=?", (s["upload_id"],), one=True)
        return FileResponse(up["stored_path"], filename=up["original_name"])
    art = s["result"].get("artifacts") or {}
    name = art.get(kind) or (art.get("fields") or {}).get(kind.removeprefix("field_"))
    if not name:
        raise HTTPException(404, "image not available")
    path = Path(s["image_dir"]) / name
    if not path.exists():
        raise HTTPException(404, "image file missing")
    return FileResponse(path, headers={"Cache-Control": "no-cache"})


@app.exception_handler(ConfigError)
def _cfg_error(_, exc):
    return JSONResponse({"detail": str(exc)}, status_code=400)


# --------------------------------------------------------------------------- frontend
@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html", headers={"Cache-Control": "no-cache"})


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
