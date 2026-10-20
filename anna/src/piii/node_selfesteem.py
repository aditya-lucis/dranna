# anna/src/piii/node_selfesteem.py — node self-talk di graph
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from anna.src.piii.selfesteem import distancing


class SelfState(TypedDict):
    messages: Annotated[list, operator.add]
    nama: str
    kritikus_terdeteksi: bool


def node_self_talk(state: SelfState) -> SelfState:
    if state.get("kritikus_terdeteksi") and state.get("nama"):
        return {
            **state,
            "messages": [
                {
                    "role": "assistant",
                    "content": distancing(state["nama"], ""),
                }
            ],
        }
    return state


builder = StateGraph(SelfState)
builder.add_node("self_talk", node_self_talk)
builder.set_entry_point("self_talk")
builder.add_edge("self_talk", END)
self_graph = builder.compile()
