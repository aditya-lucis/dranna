# anna/tests/test_boss8.py — unit test pelindung Boss Fight #8
from tools.boss8_hakim import run_boss8
from tools.boss8_evaluasi import evaluasi_checklist, CHECKLIST_BOSS8


def test_boss8_pelindung_lengkap():
    """Invarian: Boss Fight #8 harus lulus 7/7 skenario ujian sang hakim."""
    assert run_boss8() is True


def test_boss8_checklist_evaluasi():
    """Invarian: Seluruh butir audit evaluasi sang hakim harus dipenuhi."""
    assert evaluasi_checklist([True] * len(CHECKLIST_BOSS8)) is True
    assert evaluasi_checklist([True] * (len(CHECKLIST_BOSS8) - 1) + [False]) is False
