"""Web API flow: upload batch -> processing -> review/override -> approve -> export."""
import importlib
import io
import json
import time
from pathlib import Path

import cv2
import pytest


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    import os

    os.environ["OMR_DATA_DIR"] = str(tmp_path_factory.mktemp("data"))
    from fastapi.testclient import TestClient

    import omr_app.web.app as appmod

    appmod = importlib.reload(appmod)
    with TestClient(appmod.app) as c:
        yield c


def _png(synth_marks):
    from omr_app.config import load_sheet_config
    from omr_app.testing.synth import SheetSynth

    cfg = load_sheet_config()
    d = Path(cfg["_dir"])
    tpl = json.loads((d / cfg["omr_template"]).read_text())
    syn = SheetSynth(d / cfg["reference"]["pdf"], tpl, cfg["reference"]["dpi"], dpi=200, seed=5)
    img = syn.degrade(syn.make_sheet(synth_marks), rotate=0.8, noise=3, blur=3)
    return cv2.imencode(".png", img)[1].tobytes()


def test_batch_review_export(client):
    key_id = "institute_2026_business_management"
    good = _png([(q, a, "fill", 40) for q, a in zip(range(1, 11), "BCABBBBBBB")])
    multi = _png([(q, a, "fill", 40) for q, a in zip(range(1, 11), "BCABBBBBBB")] + [(5, "D", "fill", 40)])
    r = client.post("/api/batches", data={"answer_key_id": key_id, "name": "قاعة 1"},
                    files=[("files", ("طالب1.png", good, "image/png")), ("files", ("s2.png", multi, "image/png"))])
    assert r.status_code == 200, r.text
    bid = r.json()["id"]
    for _ in range(100):
        b = client.get(f"/api/batches/{bid}").json()
        if b["state"] == "done":
            break
        time.sleep(0.2)
    assert b["state"] == "done" and b["name"] == "قاعة 1"
    assert b["counts"] == {"AUTO_APPROVED": 1, "REVIEW_REQUIRED": 1}
    sheets = client.get(f"/api/batches/{bid}/sheets").json()
    rev = next(s for s in sheets if s["status"] == "REVIEW_REQUIRED")
    assert rev["answers"]["5"] == "MULTIPLE"
    # cannot approve while unresolved
    assert client.patch(f"/api/sheets/{rev['id']}", json={"approve": True}).status_code == 400
    r = client.patch(f"/api/sheets/{rev['id']}", json={"overrides": {"5": "B"}, "approve": True,
                                                       "candidate_name": "سارة", "actor": "tester"})
    assert r.status_code == 200, r.text
    s = r.json()
    assert s["status"] == "MANUALLY_REVIEWED" and s["score"] == 100
    assert s["result"]["detected_answers"]["5"] == "MULTIPLE" and s["result"]["answers"]["5"] == "B"
    assert any(a["action"] == "review" and "Q5" in a["details"] for a in s["audit"])
    # images
    assert client.get(f"/api/sheets/{rev['id']}/image/overlay").status_code == 200
    # exports
    x = client.get(f"/api/batches/{bid}/export.xlsx")
    assert x.status_code == 200 and x.content[:2] == b"PK"
    from openpyxl import load_workbook

    ws = load_workbook(io.BytesIO(x.content)).active
    rows = list(ws.values)
    assert rows[0] == ("الاختصاص", "رقم الصفحة في ملف PDF", "الاسم", "الإجابات الصحيحة", "الإجابات الخاطئة",
                       "العلامة", "العلامة القصوى", "المراجِع")
    assert all(r[0] == "إدارة الأعمال" for r in rows[1:])
    assert any(r[2] == "سارة" and r[5] == 100 and r[7] == "tester" for r in rows[1:])
    p = client.get(f"/api/batches/{bid}/export.pdf")
    assert p.status_code == 200 and p.content[:4] == b"%PDF"
    import pymupdf

    import unicodedata

    text = unicodedata.normalize("NFKC", pymupdf.open(stream=p.content, filetype="pdf")[0].get_text())  # shaped glyphs -> letters
    assert "سارة" in text and "100" in text
    assert client.get(f"/api/batches/{bid}/export.csv").status_code == 400
    # re-key the whole batch to another specialization
    b = client.post(f"/api/batches/{bid}/answer-key", json={"answer_key_id": "institute_2026_commercial_banking"}).json()
    assert b["answer_key_id"] == "institute_2026_commercial_banking"


def test_reject_unsupported_upload(client):
    r = client.post("/api/batches", data={"answer_key_id": "institute_2026_business_management"},
                    files=[("files", ("notes.txt", b"hello", "text/plain"))])
    assert r.status_code == 400
