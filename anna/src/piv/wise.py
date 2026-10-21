# anna/src/piv/wise.py — Wise Mind DBT & sintesis dialektika dua kebenaran
from langchain_core.tools import tool


def prompt_wise() -> str:
    """Menghasilkan panduan eksplorasi 3 langkah pikiran: logika, emosi, dan sintesis temu."""
    return (
        "Coba dulu: apa kata logikamu soal situasi ini? "
        "Lalu: apa kata perasaanmu? Sekarang: titik temu — "
        "apa yang kedua-duanya setuju?"
    )


def dialektika(a: str, b: str) -> str:
    """Menghubungkan dua premis berlawanan dalam satu dialektika terintegrasi."""
    return f"Dua-duanya bisa benar: {a} — DAN — {b}."


@tool
def tawarkan_wise_mind() -> str:
    """Pandu wise mind: logika + emosi → titik temu (DBT)."""
    return prompt_wise()
