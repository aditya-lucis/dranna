# anna/tests/test_kartu.py
from anna.src.piii.kartu import KARTU, tawar_kartu


def test_semua_kartu_berpenutup_rujuk():
    assert all(k.penutup_rujuk for k in KARTU)


def test_tawaran_memuat_izin_dan_bukti():
    t = tawar_kartu("gelombang-cemas")
    assert t.startswith("Mau")
    assert "lebih baik dari kartu" in t


def test_kartu_tak_dikenal_jujur():
    assert "belum ada" in tawar_kartu("tidak-ada")
