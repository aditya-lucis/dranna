# anna/tests/test_rujuk.py
from anna.src.piii.rujuk import kalimat_rujuk, JALUR


def test_empat_komponen_hadir():
    k = kalimat_rujuk("x", "id")
    for w in ("berat", "mampu", "119", "di sini"):
        assert w in k.lower() or w in k


def test_tak_ada_meninggalkan():
    k = kalimat_rujuk("x", "id")
    assert "pergi" not in k.lower() and "tinggal" not in k.lower()


def test_geo_aware():
    assert "988" in kalimat_rujuk("x", "us")
    assert "119" in kalimat_rujuk("x", "id")
