# anna/src/piv/breathing.py — panduan napas sinusoidal 10 detik, box breathing, & 4-7-8
import math
from langchain_core.tools import tool


def fase_napas(t: float, periode: float = 10.0) -> str:
    """Menghitung fase napas sinusoidal: masuk [0, pi), keluar [pi, 2*pi). t dalam detik."""
    phi = (t / periode * 2 * math.pi) % (2 * math.pi)
    return "masuk" if phi < math.pi else "keluar"


def hitungan_478() -> list[str]:
    """Mengembalikan 3 tahapan pola pernapasan parasimpatis 4-7-8."""
    return ["masuk 4", "tahan 7", "keluar 8"]


@tool
def pandu_napas(pola: str = "478", siklus: int = 4) -> str:
    """Pandu pernapasan: 478, box, atau coherent. Hitung bersama."""
    if pola == "478":
        return " | ".join(hitungan_478()) + f" × {siklus}"
    return f"Pola {pola}: masuk 5, keluar 5 × {siklus} (coherent)"
