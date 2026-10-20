# anna/src/piii/node_loneliness.py — node arah-keluar (low-frequency, high-context)
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from anna.src.piii.loneliness import arah_keluar


class LonState(TypedDict):
    messages: Annotated[list, operator.add]
    sesi_log: list
    arah_keluar_ditawarkan: bool


def maybe_arah_keluar(state: LonState) -> LonState:
    if state.get("arah_keluar_ditawarkan"):
        return state
    tawaran = arah_keluar(state.get("sesi_log", []))
    if tawaran:
        return {
            **state,
            "arah_keluar_ditawarkan": True,
            "messages": [{"role": "assistant", "content": tawaran}],
        }
    return state


builder = StateGraph(LonState)
builder.add_node("maybe", maybe_arah_keluar)
builder.set_entry_point("maybe")
builder.add_edge("maybe", END)
lon_graph = builder.compile()
