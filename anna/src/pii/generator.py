# anna/src/pii/generator.py — node generator refleksi dengan loop retry otomatis bila membeo/belok
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, END
from anna.src.pii.reflection import jenis_reflection

REFLEKSI_PROMPT = """Buat SATU kalimat reflection untuk pesan terakhir.
ATURAN: kata-kata BARU (jangan salin frasa mentah), maksud SAMA,
tanpa menambah intensitas, tanpa menyimpulkan yang tidak disebut.
Complex (menambah 1 dimensi tersirat) hanya jika diminta."""


class RefleksiState(TypedDict):
    messages: Annotated[list, operator.add]
    reflection: str
    kelas: str


def buat_node_refleksi(model):
    def refleksi(state: RefleksiState) -> RefleksiState:
        msg = state["messages"][-1]
        pesan = msg.content if hasattr(msg, "content") else str(msg.get("content", ""))
        r1 = model.invoke(REFLEKSI_PROMPT + "\nPesan: " + pesan).content
        kelas_info = jenis_reflection(r1, pesan)
        jenis = kelas_info.get("jenis", "SIMPLE")

        if jenis in ("PARROT", "BELOK"):
            # Coba ulang satu kali dengan instruksi penegasan netral
            r1 = model.invoke(
                REFLEKSI_PROMPT + "\nCoba lagi, gunakan parafrase netral. Pesan: " + pesan
            ).content
            jenis = jenis_reflection(r1, pesan).get("jenis", "SIMPLE")

        return {**state, "reflection": r1, "kelas": jenis}
    return refleksi
