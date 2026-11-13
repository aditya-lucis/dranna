# anna/tests/conftest.py — fixture pengujian Project Serenity
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
# Test suite TIDAK boleh menyentuh jaringan/LLM asli, walau .env berisi kunci Gemini.
os.environ["ANNA_FORCE_MOCK"] = "1"
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
