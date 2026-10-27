# anna/tests/test_etika_bias.py — pengujian deteksi bias demografis & stereotip
from anna.src.pvii.bias import AuditBiasDemografis


def test_bias_gender_terdeteksi():
    audit = AuditBiasDemografis()
    res = audit.periksa_teks("Laki-laki tidak boleh menangis, harus kuat.")
    assert res.mengandung_bias is True
    assert "stereotip_gender" in res.kategori_bias


def test_bias_sosioekonomi_terdeteksi():
    audit = AuditBiasDemografis()
    res = audit.periksa_teks("Wajar stres kalau miskin dan tidak punya uang.")
    assert res.mengandung_bias is True
    assert "stereotip_sosioekonomi" in res.kategori_bias


def test_respons_inklusif_lulus():
    audit = AuditBiasDemografis()
    res = audit.periksa_teks("Setiap orang terlepas dari latar belakangnya berhak mendapatkan ruang aman.")
    assert res.mengandung_bias is False
    assert len(res.kategori_bias) == 0
