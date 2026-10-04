# anna/src/pi/wiring.py — detektor distres masuk graph sebagai node pre-scan
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END
from anna.src.pi.detektor import klasifikasi, DEFAULT_W


class DeteksiState(TypedDict):
    pesan: str
    jam: int
    level_perhatian: str
    kontribusi: dict
    messages: Annotated[list, operator.add]


def buat_node_pre_scan(w=DEFAULT_W):
    def pre_scan(state: DeteksiState) -> DeteksiState:
        hasil = klasifikasi(state["pesan"], state.get("jam", 14), w)
        return {
            **state,
            "level_perhatian": hasil["level"],
            "kontribusi": hasil["kontribusi"],
        }
    return pre_scan


def router(state: DeteksiState) -> str:
    level = state.get("level_perhatian", "LANJUT")
    if level == "LANJUT":
        return "empathy"
    elif level == "YELLOW":
        return "verifikasi_lembut"
    else:
        # ORANGE dan KANDIDAT_RED diarahkan ke pertanyaan langsung
        return "pertanyaan_langsung"
