# anna/src/pii/oars.py — orkestrasi irama OARS adaptif (Open, Affirm, Reflect, Summarize, Statement)
import numpy as np
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END

MIX = {
    # [OPEN, AFFIRM, REFLECT, SUMMARY, STATEMENT]
    "tenang": [0.35, 0.15, 0.25, 0.10, 0.15],
    "sedang": [0.20, 0.20, 0.35, 0.10, 0.15],
    "lelah": [0.10, 0.25, 0.30, 0.15, 0.20],
    "distres": [0.00, 0.30, 0.25, 0.05, 0.40],
}

JENIS = ["OPEN", "AFFIRM", "REFLECT", "SUMMARY", "STATEMENT"]


def pilih_giliran(keadaan: str, streak_tanya: int = 0, rng=None) -> str:
    """Sampling jenis giliran adaptif via rejection sampling untuk menegakkan batasan streak tanya."""
    rng = rng or np.random.default_rng()
    p = np.array(MIX[keadaan], dtype=float)

    for _ in range(6):
        if p.sum() > 0:
            p = p / p.sum()
        else:
            return "STATEMENT"

        jenis = JENIS[int(rng.choice(len(JENIS), p=p))]
        tanya = jenis == "OPEN"
        if not (tanya and streak_tanya >= 2):
            return jenis
        p[JENIS.index("OPEN")] *= 0.3  # Beri penalti jika streak tanya melebihi 2

    return "STATEMENT"


class OarsState(TypedDict):
    messages: Annotated[list, operator.add]
    keadaan: str
    streak_tanya: int
    giliran: str


def node_pilih(state: OarsState) -> OarsState:
    g = pilih_giliran(state.get("keadaan", "tenang"), state.get("streak_tanya", 0))
    streak = state.get("streak_tanya", 0) + 1 if g == "OPEN" else 0
    return {**state, "giliran": g, "streak_tanya": streak}


def node_generasi(state: OarsState) -> OarsState:
    return {
        **state,
        "messages": [{"role": "assistant", "content": f"[{state['giliran']}] (generasi respon)"}],
    }


builder = StateGraph(OarsState)
builder.add_node("pilih", node_pilih)
builder.add_node("generasi", node_generasi)
builder.set_entry_point("pilih")
builder.add_edge("pilih", "generasi")
builder.add_edge("generasi", END)
oars_engine = builder.compile()


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    giliran_distres = [pilih_giliran("distres", 0, rng) for _ in range(10)]
    giliran_tenang = [pilih_giliran("tenang", 0, rng) for _ in range(10)]
    print("Irama distres (zero OPEN):", giliran_distres)
    print("Irama tenang             :", giliran_tenang)
