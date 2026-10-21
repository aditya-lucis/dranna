# anna/src/piv/hardgate.py — audit exhaustive & guard node hard-gate keselamatan
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from anna.src.piv.governor import StyleGovernor

PERSONA = ["netral", "waifu", "sister"]
ESKALASI = ["GREEN", "YELLOW", "ORANGE", "RED"]


def audit_hardgate() -> dict:
    """Menguji secara tuntas (exhaustive) seluruh kombinasi 3 Persona x 4 Eskalasi.
    Memastikan tidak ada satupun skenario di mana persona bermain peran aktif saat ORANGE atau RED.
    """
    pelanggaran = []
    for p in PERSONA:
        for e in ESKALASI:
            g = StyleGovernor()
            g.set_persona(p)
            g.set_eskalasi(e)
            aktif = g.aktif()
            if e in ("ORANGE", "RED") and aktif != "netral-tenang":
                pelanggaran.append((p, e, aktif))
    return {
        "pelanggaran": pelanggaran,
        "lolos": len(pelanggaran) == 0,
    }


class GuardState(TypedDict):
    messages: Annotated[list, operator.add]
    persona: str
    eskalasi: str


def guard_persona(state: GuardState) -> GuardState:
    """Guard node di graph yang menyuntikkan arahan gaya sistem sebelum generasi chunk."""
    gov = StyleGovernor()
    p = state.get("persona", "netral")
    e = state.get("eskalasi", "GREEN")
    gov.set_persona(p)
    gov.set_eskalasi(e)
    aktif = gov.aktif()
    pesan_persona = (
        "DIMATIKAN — bahasa netral-tenang"
        if aktif == "netral-tenang" and p != "netral"
        else "aktif"
    )
    return {
        **state,
        "messages": [
            {
                "role": "system",
                "content": f"GAYA: {aktif}. Persona {p} {pesan_persona}.",
            }
        ],
    }


b = StateGraph(GuardState)
b.add_node("guard", guard_persona)
b.set_entry_point("guard")
b.add_edge("guard", END)
guard_graph = b.compile()
