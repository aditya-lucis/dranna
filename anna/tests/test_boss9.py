# anna/tests/test_boss9.py — unit test pelindung Boss Fight #9
from tools.boss9_antarmuka import run_boss9
from tools.boss9_evaluasi import evaluasi_checklist, CHECKLIST_BOSS9


def test_boss9_pelindung_lengkap():
    """Invarian: Boss Fight #9 harus lulus 8/8 skenario antarmuka & persona multi-modal."""
    assert run_boss9() is True


def test_boss9_checklist_evaluasi():
    """Invarian: Seluruh butir audit evaluasi antarmuka harus dipenuhi."""
    assert evaluasi_checklist([True] * len(CHECKLIST_BOSS9)) is True
    assert evaluasi_checklist([True] * (len(CHECKLIST_BOSS9) - 1) + [False]) is False
