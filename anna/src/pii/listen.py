# anna/src/pii/listen.py — node mendengarkan dalam graph percakapan
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END
from anna.src.pii.inti import deteksi_inti


class DengarState(TypedDict):
    messages: Annotated[list, operator.add]
    inti: dict
    jeda_ms: int


def node_mendengarkan(state: DengarState) -> DengarState:
    """Mendeteksi inti emosi dan menetapkan jeda napas 600ms sebelum generasi respons."""
    pesan = state["messages"][-1].content if hasattr(state["messages"][-1], "content") else str(state["messages"][-1].get("content", ""))
    inti = deteksi_inti(pesan)
    return {**state, "inti": inti, "jeda_ms": 600}


def node_respons(state: DengarState) -> DengarState:
    inti_teks = state["inti"].get("inti", "")
    return {
        **state,
        "messages": [{"role": "assistant", "content": f"(menyentuh inti: {inti_teks})"}],
    }


builder = StateGraph(DengarState)
builder.add_node("dengar", node_mendengarkan)
builder.add_node("respons", node_respons)
builder.set_entry_point("dengar")
builder.add_edge("dengar", "respons")
builder.add_edge("respons", END)
pendengar_graph = builder.compile()
