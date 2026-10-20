# anna/tests/test_selfesteem.py
from anna.src.piii.selfesteem import distancing


def test_distancing_memuat_nama_dan_kata_ganti_kedua():
    t = distancing("Adit", "aku gagal")
    assert "Adit" in t and "kamu" in t


def test_distancing_bukan_pujian():
    t = distancing("Adit", "")
    assert "hebat" not in t.lower()
