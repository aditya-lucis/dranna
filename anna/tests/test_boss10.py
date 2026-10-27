# anna/tests/test_boss10.py — Pytest wrapper untuk Boss Fight #10
import pytest
from tools.boss10_paripurna import run_boss10


def test_boss_fight_10_paripurna():
    sukses = run_boss10()
    assert sukses is True, "BOSS FIGHT #10: Ujian Paripurna Dr. Anna Reed harus lulus 100%!"
