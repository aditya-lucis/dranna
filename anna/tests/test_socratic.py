# anna/tests/test_socratic.py
from anna.src.piv.socratic import pertanyaan_sokratik, JENIS, node_soc


def test_selalu_pintu_skip():
    assert "skip" in pertanyaan_sokratik("bukti")


def test_lima_jenis():
    assert len(JENIS) == 5


def test_streak_anggaran_jeda():
    s = {"messages": [], "streak": 2, "jenis": "asumsi"}
    res = node_soc(s)
    assert "jeda" in res["messages"][0]["content"]
