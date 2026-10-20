# anna/src/piii/node_trauma.py — mode trauma-aware di graph
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END


class TraumaState(TypedDict):
    messages: Annotated[list, operator.add]
    posisi_arousal: str  # "dalam" | "hyper" | "hypo"
    stabilisasi_ditawarkan: bool


def node_aware(state: TraumaState) -> TraumaState:
    if state["posisi_arousal"] in ("hyper", "hypo"):
        return {
            **state,
            "stabilisasi_ditawarkan": True,
            "messages": [
                {
                    "role": "assistant",
                    "content": (
                        "Sepertinya kamu di luar jendela sekarang. "
                        "Mau kuajak satu jangkar kecil? (skip juga oke)"
                    ),
                }
            ],
        }
    return state


builder = StateGraph(TraumaState)
builder.add_node("aware", node_aware)
builder.set_entry_point("aware")
builder.add_edge("aware", END)
trauma_graph = builder.compile()
