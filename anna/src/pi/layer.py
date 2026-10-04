# anna/src/pi/layer.py — Naive Bayes sebagai pre-scan node (bukan pengambil putusan)
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END
from anna.src.pi.naive_bayes import prediksi


class PreScanState(TypedDict):
    pesan: str
    messages: Annotated[list, operator.add]
    kandidat_kelas: str
    lanjut: bool


def pre_scan_nb(state: PreScanState) -> PreScanState:
    """Pre-scan cepat 8ms. NB hanya melabel kandidat; keputusan tetap di node keselamatan."""
    hasil = prediksi(state["pesan"])
    return {
        **state,
        "kandidat_kelas": hasil["kelas"],
        "lanjut": True,
    }


def node_keselamatan(state: PreScanState) -> PreScanState:
    if state["kandidat_kelas"] == "berat":
        return {
            **state,
            "messages": [{"role": "assistant", "content": "(verifikasi lembut dipicu)"}],
        }
    return state


builder = StateGraph(PreScanState)
builder.add_node("pre_scan", pre_scan_nb)
builder.add_node("keselamatan", node_keselamatan)
builder.set_entry_point("pre_scan")
builder.add_edge("pre_scan", "keselamatan")
builder.add_edge("keselamatan", END)
pre_scan_graph = builder.compile()
