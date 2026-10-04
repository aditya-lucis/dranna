# anna/src/pii/node_tanya.py — node pertanyaan dengan pintu keluar wajib (skip is valid)
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END
from anna.src.pii.pertanyaan import pilih_bentuk


class TanyaState(TypedDict):
    messages: Annotated[list, operator.add]
    distres: float
    bentuk: str
    pertanyaan: str


def node_pilih_bentuk(state: TanyaState) -> TanyaState:
    msg = state["messages"][-1]
    teks = msg.content if hasattr(msg, "content") else str(msg.get("content", ""))
    panjang = len(teks.split())
    return {**state, "bentuk": pilih_bentuk(state.get("distres", 0.0), panjang)}


def node_buat_tanya(state: TanyaState) -> TanyaState:
    # Setiap pertanyaan terbuka/scaling DIWAJIBKAN memiliki opsi pintu keluar 'skip juga oke'
    return {
        **state,
        "pertanyaan": f"[{state['bentuk']}] Ceritakan apa yang kamu rasakan. (skip juga oke ya)",
    }


builder = StateGraph(TanyaState)
builder.add_node("pilih", node_pilih_bentuk)
builder.add_node("tanya", node_buat_tanya)
builder.set_entry_point("pilih")
builder.add_edge("pilih", "tanya")
builder.add_edge("tanya", END)
pemilih_tanya = builder.compile()
