# anna/tests/test_tipp.py
from anna.src.piv.tipp import pilih_tipp, tawarkan_tipp


def test_kondisi_jantung_bypass_t_i():
    t = pilih_tipp({"kondisi_jantung": True})
    assert "napas" in t.lower() or "breathing" in t.lower()


def test_bisa_gerak_intense():
    t = pilih_tipp({"bisa_gerak": True})
    assert "60" in t or "intens" in t.lower()


def test_alat_tawarkan_tipp():
    res = tawarkan_tipp.invoke({"kondisi_jantung": False, "bisa_gerak": False})
    assert "Temperature" in res
