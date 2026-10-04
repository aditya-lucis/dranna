# anna/tests/test_doctor.py — verifikasi doctor lingkungan
import importlib
import sys
import pytest
from anna.src.reset import doctor as d


def test_doctor_lulus_di_env_benar():
    """Memastikan bahwa modul-modul inti September 2026 terpasang sesuai spesifikasi."""
    masalah = d.doctor(verbose=False)
    assert masalah == 0, f"Ditemukan {masalah} masalah lingkungan pada stack runtime"


def test_doctor_deteksi_kunci_hilang(monkeypatch):
    """Memastikan fungsi pendeteksi kunci API sensitif terhadap ketiadaan env."""
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    assert d._kunci_ada() is False
