# anna/src/reset/peta.py — kontrak 10 lapis sebagai satu modul
from pydantic import BaseModel

LAPIS = [
    ("ui", "Vue 3 + Tailwind 4", "streaming, avatar-status, kontrol"),
    ("api", "FastAPI 0.141", "SSE/WS, auth, rate limit"),
    ("orchestr", "LangGraph 1.2", "state graph, checkpoint, interrupt"),
    ("safety", "Safety Gate", "tangga GREEN-RED, veto chunk"),
    ("empathy", "Empathy Engine", "OARS, beban kognitif, reflection"),
    ("therapy", "Therapy Engine", "CBT/ACT/DBT/MI + fitness matrix"),
    ("knowledge", "RAG psikoedukasi", "pgvector, sumber bersitasi"),
    ("memory", "Memory PG", "buffer+ringkas+episodik, consent"),
    ("mood", "Mood Analytics", "NumPy timeline, EWMA, tanpa diagnosis"),
    ("voicevis", "Voice & Multimodal", "whisper/kokoro/mediapipe, consent"),
]


class PetaSerenity(BaseModel):
    veto_tertinggi: str = "safety"  # hanya safety yang bisa memveto semua
    arah_ketergantungan: str = "ui -> api -> orchestr -> {safety first} -> engines"

    def urutan_init(self) -> list[str]:
        # Kebalikan arah data: data & safety dibangun terlebih dahulu, UI paling akhir
        return [nama for nama, _, _ in list(reversed(LAPIS))[:4]] + ["engines", "ui"]


if __name__ == "__main__":
    print(PetaSerenity().urutan_init())
