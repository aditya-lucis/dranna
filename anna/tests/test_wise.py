# anna/tests/test_wise.py
from anna.src.piv.wise import dialektika, prompt_wise, tawarkan_wise_mind


def test_dialektika_dan():
    assert "DAN" in dialektika("a", "b")


def test_prompt_tiga_langkah():
    p = prompt_wise()
    assert "logika" in p and "perasaan" in p and "temu" in p


def test_alat_tawarkan_wise_mind():
    res = tawarkan_wise_mind.invoke({})
    assert "logika" in res
