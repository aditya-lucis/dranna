# anna/tests/test_depresi.py
import numpy as np
from anna.src.piii.depresi import refleksi_phq9_dengan_item9


def test_item9_memicu_gerbang_tanpa_peduli_skor():
    # Skor 9 = kategori 'ringan', tapi item 9 menyala (jawaban ke-9 bernilai 1)
    r = refleksi_phq9_dengan_item9(np.array([1] * 9))
    assert r["gerbang"] == "ORANGE"
    assert r["kategori"] == "ringan"


def test_tanpa_item9_tidak_gerbang():
    # Total skor 16 (sedang-berat), tapi item 9 adalah 0
    r = refleksi_phq9_dengan_item9(np.array([2, 2, 2, 2, 2, 2, 2, 2, 0]))
    assert r["gerbang"] is None


def test_pesan_gerbang_tidak_menakut_namai():
    r = refleksi_phq9_dengan_item9(np.array([0] * 8 + [1]))
    assert "boleh" in r["pesan"].lower()
