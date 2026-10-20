# anna/tests/test_loneliness.py
from anna.src.piii.loneliness import arah_keluar


def test_tawaran_keluar_muncul_saat_anna_dominan():
    log = [{"channel": "anna"}] * 15
    assert arah_keluar(log) is not None


def test_tidak_muncul_saat_masih_ada_kontak_manusia():
    log = [{"channel": "anna", "human_contact": True}] * 15
    assert arah_keluar(log) is None


def test_tidak_muncul_saat_belum_pola():
    assert arah_keluar([{"channel": "anna"}] * 3) is None
