# anna/tests/conftest.py — fixture pengujian Project Serenity
import os
import pytest


@pytest.fixture
def tidak_ada_jaringan(monkeypatch):
    """Fixture isolasi jaringan untuk memastikan pengujian keselamatan tidak bergantung layanan eksternal."""
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("LANGCHAIN_API_KEY", raising=False)
    monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)


@pytest.fixture
def mode_krisis():
    """Fixture penanda konteks darurat krisis aktif."""
    return {"level": "RED", "hard_gate": True, "sintetis": True}
