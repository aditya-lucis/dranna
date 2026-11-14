# anna/src/agent/graph.py — StateGraph LangGraph 1.2 Multi-Node Dr. Anna Reed
"""
Graph percakapan terpadu berbasis LangGraph 1.2:

    safety ──┬─ rujuk ────────────────────────────────────────────┐
             ├─ tolak ────────────────────────────────────────────┤
             └─ retrieve → terapi → generate → reflection ────────┴─ status → END

- safety     : deteksi berlapis (tangga + leksikon + logistic + jam + Item-9), Style Governor, hard-gate
- rujuk      : KANDIDAT_RED/RED → rujukan 4-komponen + hotline, deterministik (tanpa LLM, < 200 ms)
- tolak      : permintaan diagnosis/medikasi → penolakan peran, deterministik
- terapi     : pemilihan teknik (krisis → stabilisasi fisik saja; selain itu pilih_teknik(keadaan))
- generate   : LLM (Gemini / Mock) dengan system prompt ber-kontrak invarian
- reflection : self-correction etika + lampiran hotline saat hard-gate
- status     : 4 lapis status independen
"""
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage, SystemMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel

from anna.src.agent.arsitektur import CompanionState
from anna.src.agent.safety_node import (
    evaluasi_keselamatan,
    node_rujuk_darurat,
    node_tolak,
    node_status,
    rute_keselamatan,
    _baris_hotline_singkat,
    _geo,
    _teks_terakhir,
)
from anna.src.agent.reflection import evaluasi_dan_perbaiki
from anna.src.agent.provider import get_chat_model
from anna.src.agent.prompts import build_system_prompt
from anna.src.piii.retrieval import temukan_relevan
from anna.src.piv.engine import pilih_teknik

__all__ = ["create_companion_graph", "rute_keselamatan"]

PENANDA_FISIK = ("panik", "sesak", "berdebar", "napas", "nafas", "gemetar", "jantung")
PENANDA_HIPO = ("hampa", "kosong", "mati rasa", "kebas", "nggak ngerasa apa", "tidak merasa apa")
PENANDA_AMBIVALEN = ("ragu", "bimbang", "di satu sisi", "mau tapi", "pengen tapi", "antara", "nggak yakin")
PENANDA_DEPRESI = ("sedih", "hampa", "capek", "lelah", "males", "malas", "murung", "nggak semangat")


def turunkan_keadaan(teks: str, hard_gate: bool) -> str:
    tl = teks.lower()
    if hard_gate:
        return "krisis"
    if any(k in tl for k in PENANDA_AMBIVALEN):
        return "ambivalen"
    if any(k in tl for k in PENANDA_DEPRESI):
        return "tenang-depresi"
    return "default"


def pilih_teknik_giliran(teks: str, hard_gate: bool) -> tuple[str, str]:
    """Mengembalikan (keadaan, teknik). Saat hard-gate HANYA teknik stabilisasi fisik (dilarang Sistem 2)."""
    tl = teks.lower()
    keadaan = turunkan_keadaan(teks, hard_gate)
    if hard_gate:
        if any(k in tl for k in PENANDA_FISIK):
            return keadaan, "breathing_478"
        if any(k in tl for k in PENANDA_HIPO):
            return keadaan, "grounding"
        return keadaan, pilih_teknik("krisis")  # dbt_tipp

    if "gagal" in tl or "harus" in tl or "semua orang" in tl:
        return keadaan, "restrukturisasi_kognitif"
    if "tidak berguna" in tl or "capek mikir" in tl:
        return keadaan, "defusi_act"
    return keadaan, pilih_teknik(keadaan)


def buat_node_retrieve():
    def node_retrieve(state: CompanionState) -> CompanionState:
        teks = _teks_terakhir(state)
        dokumen = []
        try:
            dokumen = temukan_relevan(teks, top_k=2)
        except Exception:
            dokumen = []

        topik = list(state.get("topik_aktif", []) or [])
        if "panik" in teks.lower() and "panik" not in topik:
            topik.append("panik")
        elif "cemas" in teks.lower() and "anxietas" not in topik:
            topik.append("anxietas")

        return {
            "dokumen_retrieved": dokumen,
            "topik_aktif": topik,
        }
    return node_retrieve


def buat_node_terapi():
    def node_terapi(state: CompanionState) -> CompanionState:
        keadaan, teknik = pilih_teknik_giliran(_teks_terakhir(state), bool(state.get("hard_gate_aktif")))
        return {"keadaan": keadaan, "teknik_aktif": teknik}
    return node_terapi


def susun_input_llm(state: CompanionState) -> list[BaseMessage]:
    """System prompt + riwayat; dipakai node generate (dan dapat dipakai ulang untuk streaming token)."""
    topik_list = state.get("topik_aktif", [])
    system_text = build_system_prompt(
        persona=state.get("persona_aktif") or state.get("persona", "netral"),
        eskalasi=state.get("eskalasi", "GREEN"),
        topik=", ".join(topik_list) if topik_list else None,
        memori_ringkasan=state.get("ringkasan_memori", ""),
        metadata=state.get("metadata", {}),
        hard_gate=bool(state.get("hard_gate_aktif")),
        instruksi_gaya=state.get("instruksi_gaya"),
    )

    teknik = state.get("teknik_aktif")
    if teknik:
        system_text += f"\n[Rekomendasi Teknik Klinis]: Selipkan elemen {teknik} secara bersahaja dan menenangkan."

    docs = state.get("dokumen_retrieved", [])
    if docs and not state.get("hard_gate_aktif"):
        snippets = " | ".join([d.get("isi", "")[:120] for d in docs if isinstance(d, dict)])
        if snippets:
            system_text += f"\n[Materi Psikoedukasi Terpercaya]: {snippets}"

    chat_input: list[BaseMessage] = [SystemMessage(content=system_text)]
    chat_input.extend(state.get("messages", []))
    return chat_input


def teks_dari_konten(c) -> str:
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in c)
    return str(c)


FALLBACK_RESPONS = (
    "Aku di sini mendengarkanmu. Pelan-pelan saja, kita lewati ini satu langkah demi satu langkah."
)


def buat_node_generate(model: BaseChatModel | None = None):
    llm = model or get_chat_model()

    def node_generate(state: CompanionState) -> CompanionState:
        try:
            draft = teks_dari_konten(llm.invoke(susun_input_llm(state)).content)
        except Exception:
            draft = FALLBACK_RESPONS
        return {
            "respons_draft": draft or FALLBACK_RESPONS,
            "ekspresi_avatar": "menulis",
        }
    return node_generate


def buat_node_reflection():
    def node_reflection(state: CompanionState) -> CompanionState:
        draft = state.get("respons_draft", "")
        konteks = {
            "sitasi_terdaftar": ["NIMH", "NICE", "WHO", "SAMHSA", "Beck", "Linehan"],
        }
        eval_res = evaluasi_dan_perbaiki(draft, konteks=konteks)
        respons_final = eval_res["respons_final"]

        if state.get("hard_gate_aktif"):
            baris = _baris_hotline_singkat(_geo(state))
            if baris not in respons_final:
                respons_final = f"{respons_final}\n\n{baris}"

        eskalasi = state.get("eskalasi", "GREEN")
        ekspresi = "tenang" if eskalasi in ("ORANGE", "YELLOW") else "jeda"

        return {
            "respons_final": respons_final,
            "messages": [AIMessage(content=respons_final)],
            "ekspresi_avatar": ekspresi,
        }
    return node_reflection


def create_companion_graph(
    model: BaseChatModel | None = None,
    checkpointer=None,
):
    """Membangun StateGraph terkompilasi Dr. Anna Reed dengan seluruh proteksi safety."""
    workflow = StateGraph(CompanionState)

    workflow.add_node("safety", evaluasi_keselamatan)
    workflow.add_node("rujuk", node_rujuk_darurat)
    workflow.add_node("tolak", node_tolak)
    workflow.add_node("retrieve", buat_node_retrieve())
    workflow.add_node("terapi", buat_node_terapi())
    workflow.add_node("generate", buat_node_generate(model=model))
    workflow.add_node("reflection", buat_node_reflection())
    workflow.add_node("status", node_status)

    workflow.set_entry_point("safety")
    workflow.add_conditional_edges(
        "safety",
        rute_keselamatan,
        {"rujuk": "rujuk", "tolak": "tolak", "retrieve": "retrieve"},
    )
    workflow.add_edge("rujuk", "status")
    workflow.add_edge("tolak", "status")
    workflow.add_edge("retrieve", "terapi")
    workflow.add_edge("terapi", "generate")
    workflow.add_edge("generate", "reflection")
    workflow.add_edge("reflection", "status")
    workflow.add_edge("status", END)

    if checkpointer is not None:
        return workflow.compile(checkpointer=checkpointer)
    return workflow.compile()
