# anna/tests/test_journaling.py
from anna.src.piv.journaling import PROMPT, prompt_harian, tawarkan_journaling


def test_pintu_skip_ada():
    assert "skip" in prompt_harian(1)


def test_lima_prompt_minimal():
    assert len(PROMPT) >= 5


def test_alat_tawarkan_journaling():
    res = tawarkan_journaling.invoke({})
    assert "skip" in res
