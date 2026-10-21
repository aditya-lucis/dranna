# anna/src/piv/engine.py — registry teknik, pemilih fitness & router graph
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END

TEKNIK = {
    "cbt_thought_record": "cbt",
    "act_defusi": "act",
    "dbt_tipp": "dbt",
    "mi_oars": "mi",
    "journaling": "umum",
    "breathing": "umum",
    "grounding": "umum",
}


def pilih_teknik(keadaan: str) -> str:
    """Memilih teknik terapi berbasis kondisi emosi pengguna:
    - krisis: HANYA stabilisasi fisik (dbt_tipp)
    - ambivalen: Motivational Interviewing (mi_oars)
    - tenang-depresi: CBT thought record
    - lainnya/default: ACT defusi kognitif
    """
    if keadaan == "krisis":
        return "dbt_tipp"  # HANYA stabilisasi, dilarang Sistem 2
    if keadaan == "ambivalen":
        return "mi_oars"
    if keadaan == "tenang-depresi":
        return "cbt_thought_record"
    return "act_defusi"


class TherapyState(TypedDict):
    messages: Annotated[list, operator.add]
    keadaan: str
    teknik: str


def router(state: TherapyState) -> TherapyState:
    return {**state, "teknik": pilih_teknik(state.get("keadaan", "default"))}


b = StateGraph(TherapyState)
b.add_node("router", router)
b.set_entry_point("router")
b.add_edge("router", END)
therapy_graph = b.compile()
