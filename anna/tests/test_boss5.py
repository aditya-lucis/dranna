# anna/tests/test_boss5.py — unit test pelindung Boss Fight #5
from tools.boss5_pendamping import run_boss5
from tools.boss5_evaluasi import evaluasi_checklist, CHECKLIST_BOSS5


def test_boss5_seluruh_skenario_lulus():
    """Invarian: Boss Fight #5 harus lulus 6/6 skenario klinis & teknis."""
    assert run_boss5() is True


def test_boss5_checklist_lengkap():
    """Invarian: Seluruh poin audit reviewer harus dipenuhi."""
    assert evaluasi_checklist([True] * len(CHECKLIST_BOSS5)) is True
    assert evaluasi_checklist([True] * (len(CHECKLIST_BOSS5) - 1) + [False]) is False
