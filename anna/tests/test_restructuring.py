# anna/tests/test_restructuring.py
from anna.src.piv.restructuring import cek_seimbang, rumus_pikiran_seimbang


def test_positif_saja_ditolak():
    assert cek_seimbang("Aku hebat pasti bisa!")["seimbang"] is False


def test_dua_bukti_lulus():
    assert cek_seimbang("Tidak mulus DAN pernah baik")["seimbang"] is True


def test_alat_rumus_seimbang():
    r = rumus_pikiran_seimbang.invoke({
        "bukti_mendukung": "Hasil tes belum maksimal",
        "bukti_menentang": "Aku sudah belajar banyak konsep baru",
    })
    assert "DAN" in r
    assert "adil" in r
