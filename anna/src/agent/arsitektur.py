# anna/src/agent/arsitektur.py — kontrak state percakapan terpadu LangGraph 1.2
import operator
from typing import Annotated, TypedDict, Any
from langchain_core.messages import BaseMessage


class CompanionState(TypedDict, total=False):
    """Skema state menyeluruh pendamping digital Dr. Anna Reed."""
    messages: Annotated[list[BaseMessage], operator.add]
    sesi_id: str
    persona: str  # "netral" | "waifu" | "sister"
    eskalasi: str  # "GREEN" | "YELLOW" | "ORANGE" | "RED"
    keadaan: str
    topik_aktif: list[str]
    dokumen_retrieved: list[dict]
    teknik_aktif: str | None
    krisis_terdeteksi: bool
    ringkasan_memori: str
    respons_draft: str
    respons_final: str
    ekspresi_avatar: str  # "siap" | "mendengar" | "menyusun" | "menulis" | "tenang" | "perhatian" | "jeda"
    metadata: dict[str, Any]
