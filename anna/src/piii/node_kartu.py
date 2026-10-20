# anna/src/piii/node_kartu.py — kartu lewat graph saat pengguna setuju
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from anna.src.piii.kartu import tawar_kartu


class CopingState(TypedDict):
    messages: Annotated[list, operator.add]
    saat: str
    setuju: bool


def tawarkan(state: CopingState) -> CopingState:
    return {
        **state,
        "messages": [{"role": "assistant", "content": tawar_kartu(state["saat"])}],
    }


def dampingi(state: CopingState) -> CopingState:
    if not state.get("setuju"):
        return {
            **state,
            "messages": [
                {
                    "role": "assistant",
                    "content": "Oke — kita lewatkan dulu. Aku tetap di sini.",
                }
            ],
        }
    return state


builder = StateGraph(CopingState)
builder.add_node("tawarkan", tawarkan)
builder.add_node("dampingi", dampingi)
builder.set_entry_point("tawarkan")
builder.add_edge("tawarkan", "dampingi")
builder.add_edge("dampingi", END)
coping_graph = builder.compile()
