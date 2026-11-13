# anna/tests/test_api_sse.py — pengujian endpoint FastAPI SSE LangGraph
from fastapi.testclient import TestClient
from anna.src.api.sse import app

client = TestClient(app)


def test_sse_endpoint_get():
    with client.stream("GET", "/api/v1/sesi/sesi-test-01/stream?pesan=Halo%20Anna") as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        lines = [line for line in response.iter_lines() if line]
        assert any("event: status" in l for l in lines)
        assert any("event: chunk" in l for l in lines)
        assert any("event: selesai" in l for l in lines)


def test_sse_endpoint_post():
    payload = {
        "pesan": "Halo Anna, aku merasa sedikit lelah",
        "persona": "waifu",
        "geo": "id",
    }
    with client.stream("POST", "/api/v1/sesi/sesi-test-02/stream", json=payload) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        lines = [line for line in response.iter_lines() if line]
        assert any("event: status" in l for l in lines)


def test_consent_get_dan_post():
    user_id = "user-test-consent-01"
    # 1. Get default consent
    res = client.get(f"/api/v1/user/{user_id}/consent")
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == user_id
    assert data["izin_psikoedukasi"] is True

    # 2. Update consent
    payload = {
        "user_id": user_id,
        "izin_psikoedukasi": True,
        "izin_simpan_riwayat": False,
        "izin_analisis_mood": True,
        "durasi_simpan_hari": 30,
        "topik_sensitif_diizinkan": ["anxietas", "stres_kerja"],
    }
    res_post = client.post(f"/api/v1/user/{user_id}/consent", json=payload)
    assert res_post.status_code == 200
    assert res_post.json()["izin_simpan_riwayat"] is False
    assert "stres_kerja" in res_post.json()["topik_sensitif_diizinkan"]

    # 3. Right to be Forgotten (DELETE)
    res_del = client.delete(f"/api/v1/user/{user_id}/data")
    assert res_del.status_code == 200
    assert res_del.json()["status"] == "terhapus"
