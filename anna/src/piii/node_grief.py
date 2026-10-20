# anna/src/piii/node_grief.py — mode duka di graph (undangan cerita relasional)
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END


class DukaState(TypedDict):
    messages: Annotated[list, operator.add]
    penyebutan_kehilangan: bool
    osilasi_terlihat: bool


def node_duka(state: DukaState) -> DukaState:
    if state.get("penyebutan_kehilangan"):
        return {
            **state,
            "messages": [
                {
                    "role": "assistant",
                    "content": (
                        "Ceritakan tentang dia kalau kamu mau — bagian "
                        "mana pun yang terasa aman untuk dibuka."
                    ),
                }
            ],
        }
    return state


builder = StateGraph(DukaState)
builder.add_node("duka", node_duka)
builder.set_entry_point("duka")
builder.add_edge("duka", END)
duka_graph = builder.compile()
