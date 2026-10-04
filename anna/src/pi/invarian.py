# anna/src/pi/invarian.py — penegakan aturan proposisi sebelum generator via LangGraph guard
from typing import TypedDict
from langgraph.graph import StateGraph, END
from anna.src.pi.logika import aturan_persona_off


class GuardState(TypedDict):
    bukti_eksplisit: bool
    level: str
    persona_aktif: bool
    lanjut: bool


def guard_persona(state: GuardState) -> GuardState:
    """Guard: Menegakkan aturan SEBELUM node mana pun bicara."""
    if aturan_persona_off(state):
        return {**state, "persona_aktif": False, "lanjut": True}
    return {**state, "lanjut": True}


def node_generasi(state: GuardState) -> GuardState:
    # Generator tidak akan pernah melihat persona_aktif=True saat aturan bahaya menyala
    return state


builder = StateGraph(GuardState)
builder.add_node("guard", guard_persona)
builder.add_node("generasi", node_generasi)
builder.set_entry_point("guard")
builder.add_edge("guard", "generasi")
builder.add_edge("generasi", END)
guard_graph = builder.compile()
