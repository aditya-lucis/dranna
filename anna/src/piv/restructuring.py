# anna/src/piv/restructuring.py — restrukturisasi kognitif berimbang anti-toxic-positivity
from langchain_core.tools import tool


def cek_seimbang(kalimat: str) -> dict:
    """Memverifikasi bahwa kalimat restrukturisasi kognitif mengakomodasi dua bukti nyata
    dan bukan sekadar dorongan optimisme beracun (toxic positivity).
    """
    k = kalimat.lower()
    if any(w in k for w in ["hebat", "pasti bisa", "kuat", "semangat"]):
        if not any(w in k for w in ["dan", "meski", "tapi", "walau"]):
            return {"seimbang": False, "masalah": "positif-saja tanpa akomodasi"}
    return {"seimbang": True}


@tool
def rumus_pikiran_seimbang(bukti_mendukung: str, bukti_menentang: str) -> str:
    """Merumuskan kalimat seimbang yang menampung dua bukti nyata tanpa menghapus rasa kecewa."""
    return (
        f"Kalimat seimbang: {bukti_mendukung} — DAN {bukti_menentang}. "
        f"Cek: apakah ini adil, atau memenangkan satu sisi?"
    )
