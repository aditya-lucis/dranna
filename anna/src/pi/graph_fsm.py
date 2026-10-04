# anna/src/pi/graph_fsm.py — FSM percakapan diintegrasikan ke LangGraph StateGraph
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END


class SesiState(TypedDict):
    state_percakapan: str
    messages: Annotated[list, operator.add]
    level_perhatian: str


def buat_node(nama: str):
    def node(state: SesiState) -> SesiState:
        return {
            **state,
            "state_percakapan": nama,
            "messages": [{"role": "system", "content": f"[fase: {nama}]"}],
        }
    return node


def router_sinyal(state: SesiState) -> str:
    level = state.get("level_perhatian", "GREEN")
    if level in ("ORANGE", "KANDIDAT_RED", "RED"):
        return "SKRINING"
    return "MENDENGARKAN"


builder = StateGraph(SesiState)
for s in ("MENDENGARKAN", "SKRINING", "GROUNDING", "REFLEKSI"):
    builder.add_node(s, buat_node(s))

builder.set_entry_point("MENDENGARKAN")
builder.add_conditional_edges(
    "MENDENGARKAN",
    router_sinyal,
    {
        "MENDENGARKAN": "MENDENGARKAN",
        "SKRINING": "SKRINING",
    },
)
builder.add_edge("SKRINING", "GROUNDING")
builder.add_edge("GROUNDING", "REFLEKSI")
builder.add_edge("REFLEKSI", END)
fsm_percakapan = builder.compile()
