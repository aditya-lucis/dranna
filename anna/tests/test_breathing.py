# anna/tests/test_breathing.py
from anna.src.piv.breathing import fase_napas, hitungan_478, pandu_napas


def test_sinusoidal_masuk_keluar():
    assert fase_napas(0) == "masuk" and fase_napas(5) == "keluar"


def test_478_tiga_fase():
    assert len(hitungan_478()) == 3


def test_alat_pandu_napas():
    res_478 = pandu_napas.invoke({"pola": "478", "siklus": 3})
    assert "masuk 4" in res_478
    assert "× 3" in res_478

    res_box = pandu_napas.invoke({"pola": "box", "siklus": 2})
    assert "coherent" in res_box
