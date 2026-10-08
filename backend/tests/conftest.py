"""
Test harness for Quest Me backend. Drop into backend/tests/.

Run from backend/:   pytest -q
Needs (dev only):    pip install pytest httpx

Design notes
- Fakes Ollama at the HTTP layer by patching `requests.post`, so tests keep working
  however the code is refactored. Backend must keep using `requests` for Ollama.
- Contract the code must keep exporting:  app.main.app,
  app.models.database.{Base, engine, SessionLocal, User, Quest}
- Contract the code must honour:          env vars DATABASE_URL, UPLOAD_DIR, RATE_LIMIT_ENABLED
"""
import base64
import json as jsonlib
import os
import sys
import tempfile
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

# Isolated sandbox: set BEFORE the app is imported.
SANDBOX = Path(tempfile.mkdtemp(prefix="questme_test_"))
UPLOAD_DIR = SANDBOX / "uploads"
os.environ["DATABASE_URL"] = f"sqlite:///{SANDBOX / 'test.db'}"
os.environ["UPLOAD_DIR"] = str(UPLOAD_DIR)
os.environ["INFERENCE_MODE"] = "ollama"
os.environ["RATE_LIMIT_ENABLED"] = "0"
os.chdir(SANDBOX)  # catches code that writes to cwd-relative paths

# A real 1x1 PNG so image validation (magic bytes / Pillow) passes.
PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)

DEFAULT_QUEST = {
    "title": "Leaf Hunt",
    "description": "Find three leaves.",
    "duration_minutes": 20,
    "difficulty": "easy",
    "objectives": [
        {"id": "obj_1", "description": "Find a green leaf", "evidence_required": True},
        {"id": "obj_2", "description": "Find a dry leaf", "evidence_required": True},
    ],
    "bonus": None,
    "xp": 100,
}


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


class FakeOllama:
    """Mutable fake. Tests change .quest / .verdict / .raise_exc."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.quest = jsonlib.loads(jsonlib.dumps(DEFAULT_QUEST))
        self.verdict = {"valid": True, "confidence": 0.9, "reason": "looks right"}
        self.raise_exc = None

    def post(self, url, json=None, **kwargs):
        if self.raise_exc:
            raise self.raise_exc
        body = json or {}
        payload = self.verdict if body.get("images") else self.quest
        return FakeResponse({"response": jsonlib.dumps(payload)})


@pytest.fixture
def ollama(monkeypatch):
    fake = FakeOllama()
    monkeypatch.setattr("requests.post", fake.post)
    return fake


@pytest.fixture(autouse=True)
def fresh_db_and_uploads():
    from app.models.database import Base, engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for p in UPLOAD_DIR.rglob("*"):
        if p.is_file():
            p.unlink()
    yield


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app

    # raise_server_exceptions=False: we want to see the HTTP status a real client sees
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def total_xp():
    """Read XP straight from the DB (independent of any API shape)."""
    from app.models.database import SessionLocal, User

    def _read():
        db = SessionLocal()
        try:
            u = db.query(User).filter(User.id == 1).first()
            return u.total_xp if u else 0
        finally:
            db.close()

    return _read


def png_file(name="photo.png"):
    import io

    return {"file": (name, io.BytesIO(PNG_1X1), "image/png")}
