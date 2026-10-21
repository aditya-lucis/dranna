# anna/src/piv/opposite.py — Check the Facts & Opposite Action DBT
from langchain_core.tools import tool


def check_facts(emosi: str, fakta: str, intensitas: int) -> str:
    """Memeriksa kesesuaian intensitas emosi dengan fakta ancaman nyata di lapangan."""
    if intensitas >= 80 and "ancaman nyata" not in fakta.lower():
        return "tidak_pas"  # intensitas tinggi tanpa ancaman nyata
    return "pas"


def opposite(emosi: str) -> str:
    """Menentukan tindakan kebalikan yang sesuai dorongan afektif."""
    return {
        "takut": "mendekati (bila aman)",
        "sedih": "aktivitas ringan",
        "marah": "menurunkan intensitas/lembut",
        "bersalah": "tidak menghindar",
    }.get(emosi, "bertindak sesuai nilai")


@tool
def tawarkan_opposite_action(emosi: str, fakta: str, intensitas: int) -> str:
    """Check facts dulu; bila emosi tidak pas, tawarkan opposite action (DBT)."""
    hasil = check_facts(emosi, fakta, intensitas)
    if hasil == "pas":
        return f"Emosimu ({emosi}) tampak pas dengan fakta — bertindak sesuai."
    return (
        f"Emosi mungkin berlebih untuk fakta ini. Opposite action: {opposite(emosi)}."
    )
