# anna/tests/test_reflection.py — pengujian kualitas refleksi empati
from anna.src.pii.reflection import jenis_reflection, overlap_leksikal


def test_parrot_terdeteksi():
    """Invarian: Refleksi yang menyalin kata mentah terdeteksi sebagai PARROT."""
    pesan = "aku capek banget sama kerjaan"
    r = jenis_reflection("aku capek banget sama kerjaan", pesan, 0.90)
    assert r["jenis"] == "PARROT"


def test_kata_baru_maksud_sama():
    """Parafrase sehat: Memakai kata baru dengan kesamaan semantik tergolong SIMPLE atau COMPLEX."""
    pesan = "aku capek banget sama kerjaan"
    r = jenis_reflection("kerjaanmu menguras tenaga akhir-akhir ini", pesan, 0.60)
    assert r["jenis"] in ("SIMPLE", "COMPLEX")


def test_overlap_simetris():
    """Properti: Nilai overlap leksikal Jaccard bersifat simetris terhadap urutan kata."""
    assert overlap_leksikal("a b", "b a") == 1.0
    assert overlap_leksikal("a", "b") == 0.0
