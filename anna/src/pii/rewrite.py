# anna/src/pii/rewrite.py — penulisan ulang respon bila gagal filter empati
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END
from anna.src.pii.kegagalan import deteksi_kegagalan


class RewriteState(TypedDict):
    messages: Annotated[list, operator.add]
    kandidat: str
    lolos: bool


def buat_node_postfilter(model):
    def postfilter(state: RewriteState) -> RewriteState:
        hasil = deteksi_kegagalan(state["kandidat"])
        if hasil["tindakan"] == "lulus":
            return {**state, "lolos": True}

        # Coba perbaiki SEKALI dengan instruksi eksplisit
        prompt_revisi = (
            "Tulis ulang respons berikut TANPA saran, perbandingan penderitaan, "
            "pemaksaan rasa bersyukur, atau sanggahan. Hanya berikan validasi singkat "
            "dan penegasan kehadiran. Teks awal: " + state["kandidat"]
        )
        baru = model.invoke(prompt_revisi).content
        hasil2 = deteksi_kegagalan(baru)

        # Fallback statis 4-kata yang terjamin aman jika perbaikan kedua tetap gagal
        kandidat_final = baru if hasil2["tindakan"] == "lulus" else "Kubaca. Aku di sini."
        return {**state, "kandidat": kandidat_final, "lolos": True}

    return postfilter
