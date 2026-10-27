# anna/tests/test_eval_regresi.py — pengujian regresi OLS kestabilan empati
from anna.src.pviii.regresi import AnalisisRegresiEmpati


def test_regresi_stabil():
    skor = [4.5, 4.6, 4.5, 4.6, 4.7, 4.6, 4.5, 4.6]
    res = AnalisisRegresiEmpati.analisis_tren(skor)
    assert res["stabil"] is True
    assert res["slope"] >= -0.05
    assert res["skor_rata_rata"] >= 4.0


def test_regresi_fatigue():
    # Skor merosot drastis: 5.0 -> 2.0
    skor_drop = [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0]
    res = AnalisisRegresiEmpati.analisis_tren(skor_drop)
    assert res["stabil"] is False
    assert res["slope"] < -0.05
