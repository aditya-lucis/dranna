# anna/tests/test_hardgate.py
from anna.src.piv.hardgate import audit_hardgate, PERSONA, ESKALASI, guard_persona
from anna.src.piv.governor import StyleGovernor


def test_exhaustive_lolos():
    assert audit_hardgate()["lolos"] is True


def test_orange_red_selalu_netral():
    for p in PERSONA:
        for e in ("ORANGE", "RED"):
            g = StyleGovernor()
            g.set_persona(p)
            g.set_eskalasi(e)
            assert g.aktif() == "netral-tenang"


def test_guard_persona_injeksi_sistem():
    s = {"messages": [], "persona": "waifu", "eskalasi": "ORANGE"}
    res = guard_persona(s)
    content = res["messages"][0]["content"]
    assert "DIMATIKAN" in content
    assert "netral-tenang" in content
