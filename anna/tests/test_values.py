# anna/tests/test_values.py
from anna.src.piv.values import DOMAIN, prompt_nilai, tindakan_kecil, mulai_values_compass


def test_delapan_domain():
    assert len(DOMAIN) == 8


def test_prompt_anti_eksternal():
    p = prompt_nilai("kerja")
    assert "orang lain" in p


def test_tindakan_kecil_tidak_nyaman():
    t = tindakan_kecil("kejujuran")
    assert "tidak nyaman" in t


def test_alat_mulai_values_compass():
    res = mulai_values_compass.invoke({})
    assert "Domain" in res
