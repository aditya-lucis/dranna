# anna/tests/test_inti.py — pengujian deteksi inti active listening
from anna.src.pii.inti import deteksi_inti, skor_kalimat


def test_inti_bukan_kalimat_terakhir_ringan():
    """Active listening: Sistem memprioritaskan inti emosional berat ('kepala penuh') daripada detail fisik ringan ('badan')."""
    pesan = (
        "keluarga ngomongin masa depanku. aku cuma diam. "
        "kepala penuh nggak bisa tidur. nggak enak badan sih."
    )
    r = deteksi_inti(pesan)
    assert "badan" not in r["inti"]
    assert "tidur" in r["inti"] or "kepala" in r["inti"]


def test_kalimat_emosi_mengalahkan_kosong():
    """Skoring: Kalimat bermuatan afek dan intensitas memiliki bobot lebih tinggi dari kalimat netral."""
    assert skor_kalimat("aku kecewa banget", 0, 2) > skor_kalimat("aku", 0, 2)
