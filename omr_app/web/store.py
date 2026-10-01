"""SQLite persistence for batches, sheets (full result JSON) and the review audit trail."""
import json
import sqlite3
import threading
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    answer_key_id TEXT NOT NULL,
    created_at REAL NOT NULL,
    state TEXT NOT NULL DEFAULT 'queued',      -- queued | processing | done | error
    total_files INTEGER NOT NULL DEFAULT 0,
    processed_files INTEGER NOT NULL DEFAULT 0,
    error TEXT
);
CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
    idx INTEGER NOT NULL,
    original_name TEXT NOT NULL,
    stored_path TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'queued'
);
CREATE TABLE IF NOT EXISTS sheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
    upload_id INTEGER REFERENCES uploads(id) ON DELETE CASCADE,
    source_file TEXT NOT NULL,
    page INTEGER NOT NULL,
    candidate_id TEXT,
    candidate_name TEXT,
    answer_key_id TEXT,
    status TEXT NOT NULL,
    score REAL,
    max_score REAL,
    result_json TEXT NOT NULL,
    image_dir TEXT,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_sheets_batch ON sheets(batch_id, status);
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sheet_id INTEGER NOT NULL REFERENCES sheets(id) ON DELETE CASCADE,
    ts REAL NOT NULL,
    actor TEXT,
    action TEXT NOT NULL,
    details TEXT
);
"""


class Store:
    def __init__(self, db_path: Path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.execute("PRAGMA journal_mode = WAL")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    def q(self, sql, params=(), one=False):
        with self._lock:
            cur = self._conn.execute(sql, params)
            rows = [dict(r) for r in cur.fetchall()]
        return (rows[0] if rows else None) if one else rows

    def x(self, sql, params=()):
        with self._lock:
            cur = self._conn.execute(sql, params)
            self._conn.commit()
            return cur.lastrowid

    # ------------------------------------------------------------------ batches
    def create_batch(self, name, key_id, n_files):
        return self.x("INSERT INTO batches(name, answer_key_id, created_at, total_files) VALUES (?,?,?,?)",
                      (name, key_id, time.time(), n_files))

    def add_upload(self, batch_id, idx, original_name, stored_path):
        return self.x("INSERT INTO uploads(batch_id, idx, original_name, stored_path) VALUES (?,?,?,?)",
                      (batch_id, idx, original_name, str(stored_path)))

    def batch_counts(self, batch_id):
        rows = self.q("SELECT status, COUNT(*) n, AVG(score) avg FROM sheets WHERE batch_id=? GROUP BY status", (batch_id,))
        counts = {r["status"]: r["n"] for r in rows}
        avg = self.q("SELECT AVG(score) a FROM sheets WHERE batch_id=? AND score IS NOT NULL", (batch_id,), one=True)["a"]
        return counts, avg

    def batch(self, batch_id):
        b = self.q("SELECT * FROM batches WHERE id=?", (batch_id,), one=True)
        if b:
            b["counts"], b["avg_score"] = self.batch_counts(batch_id)
            b["total_sheets"] = sum(b["counts"].values())
        return b

    def batches(self):
        out = []
        for b in self.q("SELECT * FROM batches ORDER BY id DESC"):
            b["counts"], b["avg_score"] = self.batch_counts(b["id"])
            b["total_sheets"] = sum(b["counts"].values())
            out.append(b)
        return out

    # ------------------------------------------------------------------ sheets
    def insert_sheet(self, batch_id, upload_id, result, image_dir):
        now = time.time()
        return self.x(
            """INSERT INTO sheets(batch_id, upload_id, source_file, page, candidate_id, candidate_name, answer_key_id,
                                  status, score, max_score, result_json, image_dir, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (batch_id, upload_id, result["source_file"], result["page"], result.get("candidate_id"), result.get("candidate_name"),
             result.get("answer_key_id"), result["status"], result.get("score"), result.get("max_score"),
             json.dumps(result, ensure_ascii=False, default=str), str(image_dir), now, now),
        )

    def update_sheet(self, sheet_id, result):
        self.x(
            """UPDATE sheets SET candidate_id=?, candidate_name=?, answer_key_id=?, status=?, score=?, max_score=?,
                                 result_json=?, updated_at=? WHERE id=?""",
            (result.get("candidate_id"), result.get("candidate_name"), result.get("answer_key_id"), result["status"],
             result.get("score"), result.get("max_score"), json.dumps(result, ensure_ascii=False, default=str), time.time(), sheet_id),
        )

    def sheet(self, sheet_id):
        s = self.q("SELECT * FROM sheets WHERE id=?", (sheet_id,), one=True)
        if s:
            s["result"] = json.loads(s.pop("result_json"))
        return s

    def sheets(self, batch_id, status=None, with_result=False):
        sql = "SELECT * FROM sheets WHERE batch_id=?"
        params = [batch_id]
        if status:
            sql += " AND status=?"
            params.append(status)
        sql += " ORDER BY id"
        rows = self.q(sql, params)
        for r in rows:
            res = json.loads(r.pop("result_json"))
            if with_result:
                r["result"] = res
            else:
                r["answers"] = res.get("answers", {})
                r["correct_map"] = {str(qd["q"]): qd.get("correct") for qd in res.get("questions", [])}
                r["status_reasons"] = res.get("status_reasons", [])
        return rows

    def audit(self, sheet_id, action, details=None, actor=None):
        self.x("INSERT INTO audit(sheet_id, ts, actor, action, details) VALUES (?,?,?,?,?)",
               (sheet_id, time.time(), actor, action, json.dumps(details, ensure_ascii=False) if details is not None else None))

    def audit_log(self, sheet_id):
        rows = self.q("SELECT * FROM audit WHERE sheet_id=? ORDER BY id", (sheet_id,))
        for r in rows:
            r["details"] = json.loads(r["details"]) if r["details"] else None
        return rows
