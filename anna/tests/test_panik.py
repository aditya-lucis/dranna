# anna/tests/test_panik.py
from anna.src.piii.panik import KARTU_PANIK, kartu_darurat


def test_kartu_darurat_maksimal_tiga_baris():
    assert len(KARTU_PANIK) <= 3


def test_baris_medis_naik_pertama_kali():
    k = kartu_darurat(gejala_pertama_kali=True)
    assert "periksa medis" in k[0].lower()


def test_setiap_baris_pendek():
    assert all(len(b) <= 120 for b in KARTU_PANIK)
