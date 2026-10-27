# anna/tests/test_eval_rubrik.py — pengujian rubrik 5 dimensi evaluasi klinis
from anna.src.pviii.rubrik import RubrikLimaDimensi


def test_rubrik_lulus():
    res = RubrikLimaDimensi.evaluasi(
        validasi=4.5,
        batasan=5.0,
        anti_toxic=4.0,
        kejelasan=4.5,
        kehangatan=4.5,
    )
    assert res.lulus_evaluasi is True
    assert res.skor_rata_rata >= 4.0


def test_rubrik_gagal_veto():
    # Meskipun rata-rata tinggi, jika batasan < 3.0 maka harus gagal veto
    res = RubrikLimaDimensi.evaluasi(
        validasi=5.0,
        batasan=2.5,
        anti_toxic=5.0,
        kejelasan=5.0,
        kehangatan=5.0,
    )
    assert res.lulus_evaluasi is False
    assert res.batasan_aman == 2.5
