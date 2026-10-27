# anna/tests/test_agent_graph.py — pengujian StateGraph multi-node LangGraph
from langchain_core.messages import HumanMessage
from anna.src.agent.graph import create_companion_graph
from anna.src.agent.provider import MockGeminiChat


def test_graph_alur_krisis_short_circuit():
    graph = create_companion_graph(model=MockGeminiChat())
    state = {
        "messages": [HumanMessage(content="aku mau bunuh diri saja sekarang")],
        "persona": "waifu",
    }
    res = graph.invoke(state)
    assert res["krisis_terdeteksi"] is True
    assert res["eskalasi"] == "RED"
    assert res["persona"] in ("netral", "netral-tenang")
    assert "119" in res["respons_final"] or "bantuan" in res["respons_final"].lower()
    assert res["ekspresi_avatar"] == "perhatian"


def test_graph_alur_normal():
    graph = create_companion_graph(model=MockGeminiChat())
    state = {
        "messages": [HumanMessage(content="halo Anna, hari ini aku merasa sedikit cemas")],
        "persona": "waifu",
    }
    res = graph.invoke(state)
    assert res["krisis_terdeteksi"] is False
    assert res["eskalasi"] in ("GREEN", "YELLOW")
    assert len(res["respons_final"]) > 10
    assert len(res["messages"]) == 2  # HumanMessage + AIMessage
