# anna/tests/test_governor.py
from anna.src.piv.governor import StyleGovernor, node_gov


def test_orange_mematikan_persona():
    g = StyleGovernor()
    g.set_persona("waifu")
    g.set_eskalasi("ORANGE")
    assert g.aktif() == "netral-tenang"


def test_default_netral():
    assert StyleGovernor().aktif() == "netral"


def test_persona_invalid_ditolak():
    g = StyleGovernor()
    g.set_persona("teman")
    assert g.aktif() == "netral"


def test_node_gov_graph():
    s = {"messages": [], "persona": "sister", "eskalasi": "GREEN"}
    res = node_gov(s)
    assert "[persona_aktif: sister]" in res["messages"][0]["content"]

    s_orange = {"messages": [], "persona": "waifu", "eskalasi": "ORANGE"}
    res_orange = node_gov(s_orange)
    assert "[persona_aktif: netral-tenang]" in res_orange["messages"][0]["content"]
