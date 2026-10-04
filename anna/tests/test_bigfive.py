# anna/tests/test_bigfive.py — pengujian model vektor Big Five
import numpy as np
from anna.src.pi.bigfive import GAYA, PROFIL_DEFAULT, rekomendasi_gaya, estimasi_bigfive


def test_default_netral_tidak_memihak():
    """Invarian: Profil nol/default tidak boleh memihak ke gaya mana pun secara ekstrem."""
    skor = rekomendasi_gaya(PROFIL_DEFAULT, top=4)
    assert abs(skor[0][1]) < 0.3


def test_n_tinggi_condong_validasi():
    """Karakter: Sumbu Neuroticism (N) tinggi condong merekomendasikan validasi terlebih dahulu."""
    p = np.array([0, 0, 0, 0, 0.9])  # hanya N tinggi
    teratas = rekomendasi_gaya(p, top=1)[0][0]
    assert teratas == "validasi_dahulu"


def test_semua_vektor_gaya_valid():
    """Batas matematis: Setiap vektor gaya memiliki dimensi tepat 5 dan elemen dalam rentang [-1, 1]."""
    for nama, v in GAYA.items():
        assert v.shape == (5,) and np.all(np.abs(v) <= 1.0), nama


def test_estimator_sedikit_pesan_kembalikan_nol():
    """Kejujuran epistemik: Jika bukti sedikit, keyakinan rendah dan estimator wajib mengembalikan 0 (netral)."""
    pesan_singkat = ["hai anna", "lagi santai aja"]
    p, keyakinan = estimasi_bigfive(pesan_singkat)
    assert np.all(p == 0.0)
