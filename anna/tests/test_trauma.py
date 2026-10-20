# anna/tests/test_trauma.py
from anna.src.piii.trauma import LARANGAN, cek_kalimat_anna


def test_permintaan_detail_ditolak():
    assert cek_kalimat_anna("Ceritakan apa yang terjadi ya.") is False
    assert cek_kalimat_anna("Jelaskan detailnya sekarang.") is False


def test_kalimat_rasa_lulus():
    assert cek_kalimat_anna("Di mana rasanya sekarang?") is True
    assert (
        cek_kalimat_anna(
            "Kalau mau menyebutnya sekilas boleh, kalau tidak kita tetap bisa bekerja dengan rasanya."
        )
        is True
    )


def test_larangan_tidak_kosong():
    assert len(LARANGAN) >= 3
