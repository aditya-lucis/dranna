# anna/src/pi/narasi.py — statistik diubah menjadi narasi manusiawi (node graph)
from typing import TypedDict
from langgraph.graph import StateGraph, END


class NarasiState(TypedDict):
    ringkasan: dict
    narasi: str


def tulis_narasi(state: NarasiState) -> NarasiState:
    """Mengubah statistik numerik menjadi kalimat empatik tanpa menampilkan angka mentah."""
    r = state["ringkasan"]
    kalimat = []

    if r.get("datar_flat"):
        kalimat.append("Minggu ini rasanya datar semua ya — nggak turun naik sama sekali.")
    if r.get("min", 0.0) < -0.7:
        kalimat.append("Aku ingat ada hari yang terasa sangat berat.")
        kalimat.append("Kalau mau cerita, aku di sini — kalau tidak, juga oke.")
    if not kalimat:
        kalimat.append("Minggu ini terasa cukup seimbang. Simpan ritme baik ini ya.")

    return {**state, "narasi": " ".join(kalimat)}


builder = StateGraph(NarasiState)
builder.add_node("narasi", tulis_narasi)
builder.set_entry_point("narasi")
builder.add_edge("narasi", END)
narasi_mood = builder.compile()


if __name__ == "__main__":
    from anna.src.pi.deskriptif import ringkasan_mood
    import numpy as np

    sample = np.array([0.1, 0.0, -0.9, -0.8, 0.1, 0.2, 0.1])
    res = narasi_mood.invoke({"ringkasan": ringkasan_mood(sample), "narasi": ""})
    print("Narasi:", res["narasi"])
