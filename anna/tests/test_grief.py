# anna/tests/test_grief.py
from anna.src.piii.grief import cek_kalimat_duka


def test_moveon_dan_setidaknya_tertolak():
    assert cek_kalimat_duka("sudah waktunya move on ya")[0] is False
    assert cek_kalimat_duka("setidaknya dia tidak menderita")[0] is False
    assert cek_kalimat_duka("dia pasti ingin kamu bahagia")[0] is False


def test_undangan_cerita_lulus():
    ok, _ = cek_kalimat_duka("Ceritakan tentang dia kalau kamu mau")
    assert ok is True


def test_normalisasi_osilasi_lulus():
    ok, _ = cek_kalimat_duka("ketawa lagi bukan lupa; menangis lagi bukan mundur")
    assert ok is True
