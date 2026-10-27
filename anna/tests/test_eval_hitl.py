# anna/tests/test_eval_hitl.py — pengujian Cohen's Kappa & Human-in-the-Loop agreement
from anna.src.pviii.hitl import hitung_cohen_kappa, EvaluatorHITL


def test_cohen_kappa_sempurna():
    r1 = [1, 2, 3, 4, 5]
    r2 = [1, 2, 3, 4, 5]
    k = hitung_cohen_kappa(r1, r2)
    assert k == 1.0


def test_cohen_kappa_substantial():
    r_ai = [4, 5, 4, 3, 5, 4, 5, 4, 3, 5]
    r_hu = [4, 5, 4, 3, 5, 5, 5, 4, 4, 5]
    k = hitung_cohen_kappa(r_ai, r_hu)
    assert k >= 0.60


def test_evaluator_hitl():
    hitl = EvaluatorHITL()
    hitl.catat_penilaian_ganda("d1", 5, 5)
    hitl.catat_penilaian_ganda("d2", 4, 4)
    res = hitl.hitung_kesepakatan()
    assert res["total_sampel"] == 2
    assert res["selaras_klinis"] is True
