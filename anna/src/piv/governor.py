# anna/src/piv/governor.py — Style Governor 3 Persona (Netral/Waifu/Sister) dengan Hard-Gate
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END


class StyleGovernor:
    """Pengatur register gaya komunikasi Dr. Anna Reed dengan garansi keselamatan biner."""

    def __init__(self):
        self.persona = "netral"  # default hangat-profesional
        self.eskalasi = "GREEN"

    def set_persona(self, p: str):
        """Menyetel preferensi persona bila valid (netral, waifu, sister)."""
        if p in ("netral", "waifu", "sister"):
            self.persona = p

    def set_eskalasi(self, e: str):
        """Menyetel tingkat distres/eskalasi keselamatan sistem."""
        self.eskalasi = e

    def aktif(self) -> str:
        """Mengembalikan persona aktif.
        HARD-GATE: Saat eskalasi >= ORANGE, persona seketika OFF ke netral-tenang!
        """
        if self.eskalasi in ("ORANGE", "RED"):
            return "netral-tenang"
        return self.persona


class GovState(TypedDict):
    messages: Annotated[list, operator.add]
    persona: str
    eskalasi: str


def node_gov(state: GovState) -> GovState:
    """Node Style Governor untuk LangGraph state machine."""
    gov = StyleGovernor()
    gov.set_persona(state.get("persona", "netral"))
    gov.set_eskalasi(state.get("eskalasi", "GREEN"))
    aktif = gov.aktif()
    return {
        **state,
        "messages": [{"role": "system", "content": f"[persona_aktif: {aktif}]"}],
    }


b = StateGraph(GovState)
b.add_node("gov", node_gov)
b.set_entry_point("gov")
b.add_edge("gov", END)
gov_graph = b.compile()
