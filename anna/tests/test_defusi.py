# anna/tests/test_defusi.py
from anna.src.piv.defusi import defusi, personifikasi, tawarkan_defusi


def test_prefik_ada():
    assert "aku punya pikiran bahwa" in defusi("aku gagal")


def test_isi_tidak_diubah():
    assert "gagal" in defusi("aku gagal")


def test_personifikasi_tamu():
    p = personifikasi("aku tidak berdaya")
    assert "remote" in p


def test_alat_tawarkan_defusi():
    res = tawarkan_defusi.invoke({"pikiran": "semua berantakan"})
    assert "pikiran bahwa" in res
