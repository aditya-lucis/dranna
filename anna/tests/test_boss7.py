# anna/tests/test_boss7.py — unit test pelindung Boss Fight #7
from tools.boss7_benteng import run_boss7
from tools.boss7_evaluasi import evaluasi_checklist, CHECKLIST_BOSS7


def test_boss7_pelindung_lengkap():
    """Invarian: Boss Fight #7 harus lulus 8/8 skenario benteng etika & privasi."""
    assert run_boss7() is True


def test_boss7_checklist_evaluasi():
    """Invarian: Seluruh poin audit reviewer harus dipenuhi."""
    assert evaluasi_checklist([True] * len(CHECKLIST_BOSS7)) is True
    assert evaluasi_checklist([True] * (len(CHECKLIST_BOSS7) - 1) + [False]) is False
