# anna/tests/test_boss4.py — Boss Fight #4 Percakapan Terapeutik test suite
from tools.boss4_terapi import SKENARIO, jalankan
from tools.boss4_review import REVIEW, evaluasi_review


def test_tidak_ada_sistem2_saat_distres():
    """Veto biner: Teknik kognitif Sistem 2 (CBT / Socratic) dilarang mutlak saat distres ORANGE/RED."""
    for _, e, h in SKENARIO:
        if e in ("ORANGE", "RED"):
            assert h not in ("cbt", "socratic")


def test_lulus_konjungsi():
    """Seluruh 7 kriteria dan 8 giliran skenario harus lulus bersamaan."""
    res = jalankan()
    assert res["teknik_ok"] is True
    assert res["gate_ok"] is True
    assert res["rujuk_ok"] is True


def test_reviewer_checklist():
    """Checklist reviewer manusia memuat 6 butir etika non-negosiasi."""
    assert len(REVIEW) == 6
    assert evaluasi_review([True] * 6) is True
    assert evaluasi_review([True] * 5 + [False]) is False
