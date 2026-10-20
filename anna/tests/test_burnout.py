# anna/tests/test_burnout.py
from anna.src.piii.burnout import neraca_mingguan


def test_defisit_kronis_terdeteksi():
    r = neraca_mingguan({"lembur_berulang": 3, "oncall": 1})
    assert r["tren"] == "defisit-kronis"


def test_minggu_seimbang_cukup():
    r = neraca_mingguan({"tidur_cukup": 5, "olahraga": 3})
    assert r["tren"] == "cukup"


def test_struktur_tanpa_vonis():
    r = neraca_mingguan({"oncall": 2})
    assert "burnout" not in str(r)
