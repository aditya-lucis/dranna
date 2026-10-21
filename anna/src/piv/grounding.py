# anna/src/piv/grounding.py — Grounding Engine 5-4-3-2-1 interaktif adaptif (hyper vs hypo)
from langchain_core.tools import tool

INDRA = [
    ("dilihat", 5),
    ("disentuh", 4),
    ("didengar", 3),
    ("dicium", 2),
    ("dicicip", 1),
]


def prompt_indra(i: int) -> str:
    """Mengembalikan prompt per indra (satu indra per giliran) dengan pintu skip."""
    if i >= len(INDRA):
        return "Selesai. Bagaimana rasanya sekarang?"
    nama, n = INDRA[i]
    return f"Sebut {n} hal yang kamu {nama} sekarang. (skip juga oke)"


def adaptif(sisi: str) -> str:
    """Menyesuaikan orientasi grounding: sensorik-pasif untuk hyperarousal vs sensorik-gerakan untuk hypoarousal."""
    if sisi == "hypo":
        return (
            "Coba yang aktif: tekan kaki ke lantai, genggam jari "
            "sampai hangat, gerakkan bahu 3 kali. Sensorik-gerakan."
        )
    return prompt_indra(0)


@tool
def mulai_grounding(sisi: str = "hyper") -> str:
    """Mulai 5-4-3-2-1 grounding (adaptif hyper/hypo). Satu indra per giliran."""
    return adaptif(sisi)
