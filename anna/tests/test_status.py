# anna/tests/test_status.py — pengujian hierarki prioritas 4 lapis status interaksi
from anna.src.pii.status import Interaksi, Keselamatan, StatusBertingkat, Teknis


def test_keselamatan_menang_semua():
    """Invarian keselamatan: Lapisan keselamatan selalu menang atas teknis, interaksi, dan presentasi."""
    s = StatusBertingkat(
        teknis=Teknis.GAGAL,
        interaksi=Interaksi.MENULIS,
        keselamatan=Keselamatan.PENTING,
    )
    lapis_aktif, _ = s.tampil()
    assert lapis_aktif == "keselamatan"


def test_gate_memaksa_mode_tenang():
    """Kontrak visual: Pengaktifan gerbang keselamatan memaksa mode presentasi menjadi 'tenang'."""
    s = StatusBertingkat(interaksi=Interaksi.MENULIS)
    s.keselamatan = Keselamatan.MEMERIKSA
    s.tampil()
    assert s.presentasi_mode == "tenang"


def test_teknis_jujur_menang_dari_interaksi():
    """Kejujuran mesin: Kendala teknis (retry/gagal) menang atas klaim interaksi ('menulis')."""
    s = StatusBertingkat(teknis=Teknis.RETRY, interaksi=Interaksi.MENULIS)
    lapis_aktif, teks = s.tampil()
    assert lapis_aktif == "teknis"
    assert "retry" in teks
