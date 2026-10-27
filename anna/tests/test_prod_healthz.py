# anna/tests/test_prod_healthz.py — Unit test endpoint health, readyz, dan status klinis
import pytest
from fastapi.testclient import TestClient
from anna.src.api.sse import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz_liveness(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


def test_readyz_readiness(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.json()
    assert data["siap"] is True
    assert data["subsistem"]["tangga_risiko"] == "OK"
    assert data["subsistem"]["guardrails"] == "OK"


def test_status_klinis(client):
    response = client.get("/status/klinis")
    assert response.status_code == 200
    data = response.json()
    assert "total_request" in data
    assert "latensi_p50_ms" in data


def test_metrics_prometheus_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "anna_requests_total" in response.text
    assert response.headers["content-type"].startswith("text/plain")
