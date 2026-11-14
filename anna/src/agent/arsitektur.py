# anna/src/agent/arsitektur.py — kontrak state percakapan terpadu LangGraph 1.2
import operator
from typing import Annotated, TypedDict, Any
from langchain_core.messages import BaseMessage


class CompanionState(TypedDict, total=False):
    """Skema state menyeluruh pendamping digital Dr. Anna Reed."""
    messages: Annotated[list[BaseMessage], operator.add]
    sesi_id: str

    # Input per giliran
    jam: int | None  # jam lokal pengguna 0-23 (None = tidak diketahui, faktor jam rawan tidak dipakai)
    persona_preferensi: str  # pilihan sadar pengguna: "netral" | "waifu" | "sister"

    # Persona (kompatibilitas: `persona` = persona AKTIF hasil Style Governor)
    persona: str  # "netral" | "waifu" | "sister" | "netral-tenang"
    persona_aktif: str
    preferensi_gaya: str  # Fase 4: "auto" | "pendengar_tenang" | "ringan_playful" | dll
    gaya_komunikasi: str  # Register gaya aktif hasil Style Governor v2
    instruksi_gaya: str  # Pedoman prompt gaya hasil evaluasi Governor v2

    # Deteksi & keselamatan
    eskalasi: str  # "GREEN" | "YELLOW" | "ORANGE" | "KANDIDAT_RED" | "RED"
    sinyal_risiko: list[str]
    p_distres: float
    kontribusi_fitur: dict[str, float]
    item9_flag: bool  # pemicu satu-kali dari PHQ-9 Item-9 positif (dikonsumsi oleh node safety)
    krisis_terdeteksi: bool  # True = jalur emergency (template, tanpa LLM)
    hard_gate_aktif: bool  # True saat eskalasi >= ORANGE atau masa cooldown pasca-krisis
    cooldown_sisa: int  # sisa giliran hard-gate dipertahankan setelah krisis (persist via checkpointer)
    hotline: list[dict[str, str]] | None
    jenis_penolakan: str | None  # None | "diagnosis" | "medis"

    # Routing terapi
    keadaan: str  # "krisis" | "ambivalen" | "tenang-depresi" | "default"
    topik_aktif: list[str]
    dokumen_retrieved: list[dict]
    teknik_aktif: str | None

    # Output
    ringkasan_memori: str
    respons_draft: str
    respons_final: str
    ekspresi_avatar: str  # "siap" | "mendengar" | "menyusun" | "menulis" | "tenang" | "perhatian" | "jeda"
    status_layer: dict[str, str]  # 4 lapis: keselamatan / teknis / interaksi / presentasi
    metadata: dict[str, Any]
