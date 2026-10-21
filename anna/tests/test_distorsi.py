# anna/tests/test_distorsi.py
from anna.src.piv.distorsi import deteksi, tawar_distorsi


def test_selalu_all_or_nothing():
    assert "all_or_nothing" in deteksi("aku selalu gagal")


def test_harus_should():
    assert "should" in deteksi("aku harusnya lebih baik")


def test_tawar_distorsi_pintu():
    t = tawar_distorsi("aku selalu gagal")
    assert "pikiran hitam-putih" in t
    assert "100%" in t
