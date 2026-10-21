# anna/src/piv/socratic.py — engine pertanyaan Sokratik 5 jenis (Overholser)
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END

JENIS = ["clarifikasi", "asumsi", "perspektif_alt", "konsekuensi", "bukti"]

TEMPLATE = {
    "clarifikasi": "Apa maksudmu dengan '{konsep}'?",
    "asumsi": "Apa yang membuatmu yakin itu?",
    "perspektif_alt": "Ada cara lain melihat situasi ini?",
    "konsekuensi": "Kalau pikiran itu benar, apa artinya buat kamu?",
    "bukti": "Apa bukti yang mendukung? Yang menentang?",
}


def pertanyaan_sokratik(jenis: str, konteks: dict = None) -> str:
    """Menghasilkan pertanyaan Sokratik terstruktur berpintu skip wajib."""
    t = TEMPLATE.get(jenis, TEMPLATE["clarifikasi"])
    if konteks and "{konsep}" in t:
        t = t.format(konsep=konteks.get("konsep", "itu"))
    elif "{konsep}" in t:
        t = t.format(konsep="itu")
    return t + " (skip juga oke)"


class SocState(TypedDict):
    messages: Annotated[list, operator.add]
    streak: int
    jenis: str


def node_soc(state: SocState) -> SocState:
    """Node pembatas anggaran pertanyaan Sokratik (maksimal 2 berturut-turut)."""
    if state.get("streak", 0) >= 2:
        return {
            **state,
            "messages": [
                {
                    "role": "assistant",
                    "content": "Mungkin kita jeda dulu — banyak pertanyaan.",
                }
            ],
        }
    return {
        **state,
        "streak": state.get("streak", 0) + 1,
        "messages": [
            {
                "role": "assistant",
                "content": pertanyaan_sokratik(state.get("jenis", "clarifikasi")),
            }
        ],
    }


b = StateGraph(SocState)
b.add_node("soc", node_soc)
b.set_entry_point("soc")
b.add_edge("soc", END)
socratic_graph = b.compile()
