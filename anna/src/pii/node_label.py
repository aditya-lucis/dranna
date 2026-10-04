# anna/src/pii/node_label.py — node labeling emosi di graph (konfirmasi -> memori)
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END
from anna.src.pii.label import tawarkan_label, kalimat_tawaran


class LabelState(TypedDict):
    messages: Annotated[list, operator.add]
    pad: tuple[float, float]
    label_konfirmasi: str | None


def node_tawar(state: LabelState) -> LabelState:
    kandidat = tawarkan_label(state["pad"])
    return {
        **state,
        "messages": [{"role": "assistant", "content": kalimat_tawaran(kandidat)}],
    }


def node_selesai(state: LabelState) -> LabelState:
    # Label masuk memori jangka panjang HANYA dari konfirmasi sadar pengguna (verbal-first)
    return state


builder = StateGraph(LabelState)
builder.add_node("tawar", node_tawar)
builder.add_node("selesai", node_selesai)
builder.set_entry_point("tawar")
builder.add_edge("tawar", "selesai")
builder.add_edge("selesai", END)
labeler_graph = builder.compile()
