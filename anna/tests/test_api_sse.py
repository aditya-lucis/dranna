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
