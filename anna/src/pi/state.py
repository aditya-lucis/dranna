# anna/src/pi/state.py — keadaan emosi percakapan (LangChain / LangGraph state)
from typing import Annotated, TypedDict
import operator
from anna.src.pi.circumplex import KATA


class EmosiState(TypedDict):
    messages: Annotated[list, operator.add]
    valensi: float
    arousal: float
    label_dari_pengguna: str | None


def estimasi_dari_kata(state: EmosiState) -> EmosiState:
    """Estimasi PAD dari kata terakhir pengguna (lookup KATA).
    Prinsip: Kata pengguna MENAMAI; pad hanya MELACAK.
    Estimasi diam-diam dilarang — jika tidak ada kata yang cocok, jangan menebak.
    """
    if not state.get("messages"):
        return state

    kata_terakhir = state["messages"][-1].content.lower()
    pad_koordinat = None
    label_terpilih = None

    for k in KATA:
        if k in kata_terakhir:
            pad_koordinat = KATA[k]
            label_terpilih = k
            break

    if pad_koordinat is None:
        return state  # Biarkan label kosong, jangan menebak

    return {
        **state,
        "valensi": pad_koordinat[0],
        "arousal": pad_koordinat[1],
        "label_dari_pengguna": label_terpilih,
    }
