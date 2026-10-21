# anna/tests/test_grounding.py
from anna.src.piv.grounding import INDRA, adaptif, prompt_indra, mulai_grounding


def test_lima_indra():
    assert len(INDRA) == 5


def test_hypo_aktif_gerakan():
    t = adaptif("hypo")
    assert "kaki" in t or "genggam" in t


def test_pintu_skip():
    assert "skip" in prompt_indra(0)


def test_alat_mulai_grounding():
    res_hyper = mulai_grounding.invoke({"sisi": "hyper"})
    assert "5 hal" in res_hyper

    res_hypo = mulai_grounding.invoke({"sisi": "hypo"})
    assert "Sensorik-gerakan" in res_hypo
