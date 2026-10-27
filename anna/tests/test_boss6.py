# anna/tests/test_boss6.py — unit test pelindung Boss Fight #6
from tools.boss6_penyelamat import run_boss6
from tools.boss6_evaluasi import evaluasi_checklist, CHECKLIST_BOSS6


def test_boss6_pelindung_lengkap():
    """Invarian: Boss Fight #6 harus lulus 8/8 skenario proteksi krisis."""
    assert run_boss6() is True


def test_boss6_checklist_evaluasi():
    """Invarian: Seluruh poin audit reviewer harus dipenuhi."""
    assert evaluasi_checklist([True] * len(CHECKLIST_BOSS6)) is True
    assert evaluasi_checklist([True] * (len(CHECKLIST_BOSS6) - 1) + [False]) is False
