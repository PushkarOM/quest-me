"""
Quest Me backend acceptance tests.
Each test maps to an issue ID in QUEST_ME_FIX_PROMPT.md (see the id in the docstring).
All of these are expected to FAIL on the current code base and PASS when the prompt is done.
"""
import io

from conftest import SANDBOX, UPLOAD_DIR, png_file


# ---------- helpers ----------
def generate(client):
    r = client.post("/api/quests/generate")
    assert r.status_code == 200, r.text
    return r.json()


def upload(client, quest_id, objective_id, files=None):
    return client.post(
        f"/api/quests/{quest_id}/objectives/{objective_id}/evidence",
        files=files or png_file(),
    )


def run_full_loop(client):
    q = generate(client)
    assert client.post(f"/api/quests/{q['id']}/start").status_code == 200
    for obj in q["objectives"]:
        r = upload(client, q["id"], obj["id"])  # id EXACTLY as the frontend receives it
        assert r.status_code == 200, r.text
        assert r.json()["valid"] is True
    return q


# ---------- works at all ----------
def test_health(client):
    assert client.get("/health").status_code == 200


def test_B3_core_loop_happy_path(client, ollama, total_xp):
    """B1-B3: generate -> start -> evidence (ids as returned) -> complete -> XP awarded once."""
    q = run_full_loop(client)
    r = client.post(f"/api/quests/{q['id']}/complete")
    assert r.status_code == 200, r.text
    assert r.json()["total_xp"] == q["xp"]
    assert total_xp() == q["xp"]


def test_B4_cors_allows_dev_origin_only(client):
    ok = client.options(
        "/api/quests/generate",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"},
    )
    assert ok.headers.get("access-control-allow-origin") == "http://localhost:5173"
    bad = client.options(
        "/api/quests/generate",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"},
    )
    assert bad.headers.get("access-control-allow-origin") in (None, "")


# ---------- LLM output must not be trusted (S2) ----------
def test_S2_llm_cannot_set_arbitrary_xp(client, ollama):
    ollama.quest["xp"] = 999_999
    q = generate(client)
    assert 0 < q["xp"] <= 500


def test_S2_empty_objectives_not_accepted(client, ollama):
    ollama.quest["objectives"] = []
    r = client.post("/api/quests/generate")
    assert r.status_code != 200 or len(r.json()["objectives"]) >= 1


def test_S2_cannot_complete_without_evidence(client, ollama, total_xp):
    ollama.quest["objectives"] = [{"id": "o1", "description": "x", "evidence_required": False}]
    q = generate(client)
    client.post(f"/api/quests/{q['id']}/start")
    r = client.post(f"/api/quests/{q['id']}/complete")
    assert r.status_code in (400, 409), "quest with no verified evidence must not pay out"
    assert total_xp() == 0


def test_S2_duplicate_objective_ids_do_not_crash(client, ollama):
    ollama.quest["objectives"] = [
        {"id": "o1", "description": "a", "evidence_required": True},
        {"id": "o1", "description": "b", "evidence_required": True},
    ]
    q = generate(client)
    ids = [o["id"] for o in q["objectives"]]
    assert len(ids) == len(set(ids)) == 2


def test_S7_theme_is_bounded(client, ollama):
    r = client.post("/api/quests/generate", params={"theme": "x" * 5000})
    assert r.status_code == 422


# ---------- state machine / XP replay (S3) ----------
def test_S3_xp_awarded_exactly_once(client, ollama, total_xp):
    q = run_full_loop(client)
    client.post(f"/api/quests/{q['id']}/complete")
    after_first = total_xp()
    client.post(f"/api/quests/{q['id']}/complete")           # repeat
    client.post(f"/api/quests/{q['id']}/start")              # reopen attempt
    client.post(f"/api/quests/{q['id']}/complete")           # repeat again
    assert total_xp() == after_first == q["xp"]


def test_S3_evidence_requires_started_quest(client, ollama):
    q = generate(client)
    r = upload(client, q["id"], q["objectives"][0]["id"])
    assert r.status_code == 409


def test_S3_unknown_quest_is_404(client):
    assert client.post("/api/quests/does-not-exist/start").status_code == 404
    assert client.post("/api/quests/does-not-exist/complete").status_code == 404


# ---------- vision verdict must fail closed (S4) ----------
def test_S4_rejected_photo_blocks_completion(client, ollama):
    ollama.verdict = {"valid": False, "confidence": 0.2, "reason": "not a leaf"}
    q = generate(client)
    client.post(f"/api/quests/{q['id']}/start")
    for obj in q["objectives"]:
        r = upload(client, q["id"], obj["id"])
        assert r.status_code == 200 and r.json()["valid"] is False
    assert client.post(f"/api/quests/{q['id']}/complete").status_code in (400, 409)


def test_S4_string_false_is_not_truthy(client, ollama):
    ollama.verdict = {"valid": "false", "confidence": 0.1, "reason": "no"}
    q = generate(client)
    client.post(f"/api/quests/{q['id']}/start")
    for obj in q["objectives"]:
        upload(client, q["id"], obj["id"])
    assert client.post(f"/api/quests/{q['id']}/complete").status_code in (400, 409)


def test_S4_garbage_verdict_fails_closed_not_500(client, ollama):
    ollama.verdict = {"answer": "yes"}
    q = generate(client)
    client.post(f"/api/quests/{q['id']}/start")
    r = upload(client, q["id"], q["objectives"][0]["id"])
    assert r.status_code in (200, 502)
    if r.status_code == 200:
        assert r.json()["valid"] is False


# ---------- uploads (S5) ----------
def _started(client):
    q = generate(client)
    client.post(f"/api/quests/{q['id']}/start")
    return q, q["objectives"][0]["id"]


def test_S5_rejects_non_images(client, ollama):
    q, oid = _started(client)
    files = {"file": ("evil.exe", io.BytesIO(b"MZ\x90\x00not an image"), "text/plain")}
    assert upload(client, q["id"], oid, files).status_code in (400, 415, 422)


def test_S5_size_limit(client, ollama):
    q, oid = _started(client)
    files = {"file": ("big.png", io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"0" * (30 * 1024 * 1024)), "image/png")}
    assert upload(client, q["id"], oid, files).status_code in (400, 413, 422)


def test_S5_client_filename_cannot_escape(client, ollama):
    for evil in ("../../pwned.png", "..\\..\\pwned.png", "/etc/pwned.png", "a/b/c.png"):
        q, oid = _started(client)
        r = upload(client, q["id"], oid, png_file(evil))
        assert r.status_code != 500, f"{evil!r} caused a server error"
    leaked = [p for p in SANDBOX.rglob("pwned*")]
    assert not leaked, f"file escaped upload dir: {leaked}"


def test_S5_photos_deleted_after_verification(client, ollama):
    """Privacy: docs promise photos are not kept. Only the verdict is stored."""
    q, oid = _started(client)
    assert upload(client, q["id"], oid).status_code == 200
    assert [p for p in UPLOAD_DIR.rglob("*") if p.is_file()] == []


# ---------- errors (S6) ----------
def test_S6_error_detail_does_not_leak_internals(client, ollama):
    ollama.raise_exc = ConnectionError("HTTPConnectionPool(host='localhost', port=11434): refused")
    r = client.post("/api/quests/generate")
    assert r.status_code in (502, 503, 500)
    assert "11434" not in r.text and "localhost" not in r.text
