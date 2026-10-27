# anna/tests/test_eval_metrik.py — pengujian metrik kuantitatif empati & diversitas leksikal
from anna.src.pviii.metrik import hitung_skor_empati_leksikal, diversitas_kosakata, rasio_keseimbangan


def test_skor_empati_leksikal():
    teks_empati = "Aku mendengar betapa tidak mudahnya situasi ini. Kita pelan-pelan hadapi ini bersama."
    skor = hitung_skor_empati_leksikal(teks_empati)
    assert skor >= 0.60

    teks_dingin = "Data telah dicatat ke dalam database."
    skor_dingin = hitung_skor_empati_leksikal(teks_dingin)
    assert skor_dingin == 0.0


def test_diversitas_kosakata_ttr():
    teks_kaya = "Setiap langkah kecil yang kamu ambil hari ini memiliki arti berharga."
    ttr = diversitas_kosakata(teks_kaya)
    assert ttr >= 0.80

    teks_repetitif = "halo halo halo halo halo halo"
    ttr_rendah = diversitas_kosakata(teks_repetitif)
    assert ttr_rendah < 0.30


def test_rasio_keseimbangan():
    # Respons seimbang (20 kata vs 15 kata)
    assert rasio_keseimbangan(15, 20) == 1.0
    # Respons terlalu singkat (2 kata vs 20 kata input)
    assert rasio_keseimbangan(20, 2) <= 0.75
