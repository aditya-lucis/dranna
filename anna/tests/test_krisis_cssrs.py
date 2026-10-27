# anna/tests/test_krisis_cssrs.py — pengujian Columbia Protocol C-SSRS digital
from anna.src.pvi.cssrs import CSSRSEngine


def test_cssrs_level1():
    engine = CSSRSEngine()
    res = engine.nilai_teks("seandainya aku tidur selamanya dan tidak bangun lagi")
    assert res.level_ideasi == 1
    assert res.kategori_triage == "waspada"


def test_cssrs_level3():
    engine = CSSRSEngine()
    res = engine.nilai_teks("aku mikirin cara minum obat untuk mati")
    assert res.level_ideasi == 3
    assert res.kategori_triage == "tinggi"


def test_cssrs_level5():
    engine = CSSRSEngine()
    res = engine.nilai_teks("aku ada rencana mau loncat dan sudah tentukan tanggal")
    assert res.level_ideasi == 5
    assert res.ada_rencana is True
    assert res.kategori_triage == "ekstrem"


def test_cssrs_persiapan():
    engine = CSSRSEngine()
    res = engine.nilai_teks("kemarin aku sudah nulis surat wasiat dan bagi-bagi barang")
    assert res.ada_tindakan_persiapan is True
    assert res.kategori_triage in ("tinggi", "ekstrem")
