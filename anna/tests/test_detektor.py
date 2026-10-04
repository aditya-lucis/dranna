# anna/tests/test_detektor.py — pengujian detektor distres berjenjang
import numpy as np
from anna.src.pi.detektor import klasifikasi, DEFAULT_W


def test_pesan_berat_jam_rawan_naik_level():
    """Keselamatan: Pesan distres di jam rawan (02:00) menaikkan level perhatian dari LANJUT."""
    res = klasifikasi("aku nggak sanggup lagi", 2, DEFAULT_W)
    assert res["level"] != "LANJUT"
    assert res["p"] > 0.40


def test_pesan_ringan_lanjut():
    """Efisiensi: Pesan sehari-hari pada jam kerja normal tetap berstatus LANJUT."""
    res = klasifikasi("makan siang enak", 14, DEFAULT_W)
    assert res["level"] == "LANJUT"
    assert res["p"] < 0.20


def test_mesin_tidak_bisa_red_sendirian():
    """Invarian keselamatan: Mesin hanya boleh sampai KANDIDAT_RED; RED penuh butuh bukti eksplisit."""
    res = klasifikasi("nggak ada gunanya semuanya dan hampa banget", 3, DEFAULT_W)
    assert res["level"] != "RED"
    assert "KANDIDAT" in res["level"] or res["level"] == "ORANGE"
