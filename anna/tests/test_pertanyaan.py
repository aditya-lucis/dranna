# anna/tests/test_pertanyaan.py — pengujian bentuk pertanyaan & batas anggaran interogasi
from anna.src.pii.pertanyaan import audit_anggaran, klasifikasi_pertanyaan, pilih_bentuk


def test_kenapa_ditandai():
    """Invarian bahasa: Pertanyaan yang diawali 'kenapa' ditandai untuk diganti karena berkesan interogatif."""
    assert klasifikasi_pertanyaan("Kenapa kamu begitu?") == "WHY—ganti"


def test_distres_tinggi_tanpa_pertanyaan():
    """Anggaran kognitif: Pada distres tinggi (0.9), sistem beralih ke pernyataan/refleksi murni tanpa pertanyaan."""
    assert "PERNYATAAN" in pilih_bentuk(0.9, 10)


def test_anggaran_menolak_kuesioner():
    """Pencegahan kuesioner: Sesi dengan rasio pertanyaan > 40% otomatis ditolak oleh audit anggaran."""
    g = ["a?", "b?", "c?", "d?", "e", "f?", "g?", "h?"]
    assert audit_anggaran(g)["lolos"] is False


def test_anggaran_sehat_lolos():
    """Sesi sehat: Rasio <= 40% (1 pertanyaan dari 4 giliran = 25%) dan streak <= 2 lulus audit."""
    g = ["aku mendengarkan", "apa yang paling berat? (skip ok)", "kecewamu nyata", "aku tetap di sini"]
    assert audit_anggaran(g)["lolos"] is True
