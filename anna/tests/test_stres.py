# anna/tests/test_stres.py
from anna.src.piii.stres import refleksi_harian


def test_defisit_besar_bicara_pembayaran():
    t = refleksi_harian({"konflik": 2, "deadline": 2})
    assert "pembayaran" in t


def test_seimbang_tanpa_vonis():
    t = refleksi_harian({"jalan_santai": 2, "hobi": 1})
    assert "cukup" in t


def test_sedikit_defisit_normal():
    t = refleksi_harian({"deadline": 1, "jalan_santai": 1})
    assert "normal" in t
