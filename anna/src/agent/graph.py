# anna/src/agent/graph.py — StateGraph LangGraph 1.2 Multi-Node Dr. Anna Reed
"""
Graph percakapan terpadu berbasis LangGraph 1.2:
- Router Keselamatan (evaluasi risiko & short-circuit krisis)
- Node Retrieval (pengambilan bukti korpus psikoedukasi)
- Node Terapi Terkalibrasi (CBT / ACT / DBT)
- Node Pembangkit Respons (LLM / Gemini)
- Node Refleksi Etika (Trauma-informed, Continuing Bonds, Citations)
"""
from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel

from anna.src.agent.arsitektur import CompanionState
from anna.src.agent.safety_node import evaluasi_keselamatan, node_rujuk_darurat
from anna.src.agent.reflection import evaluasi_dan_perbaiki
from anna.src.agent.provider import get_chat_model
from anna.src.agent.prompts import build_system_prompt
from anna.src.piii.retrieval import temukan_relevan
from anna.src.piv.engine import EngineTerapi


def rute_keselamatan(state: CompanionState) -> Literal["rujuk", "retrieve"]:
    """Conditional edge: mengalihkan alur bila krisis terdeteksi."""
    if state.get("krisis_terdeteksi", False):
        return "rujuk"
    return "retrieve"


def buat_node_retrieve():
    def node_retrieve(state: CompanionState) -> CompanionState:
        messages = state.get("messages", [])
        teks = ""
        if messages:
            c = messages[-1].content
            teks = c if isinstance(c, str) else str(c)

        dokumen = []
        try:
            dokumen = temukan_relevan(teks, top_k=2)
        except Exception:
            dokumen = []

        topik = state.get("topik_aktif", [])
        if "panik" in teks.lower() and "panik" not in topik:
            topik = topik + ["panik"]
        elif "cemas" in teks.lower() and "anxietas" not in topik:
            topik = topik + ["anxietas"]

        return {
            "dokumen_retrieved": dokumen,
            "topik_aktif": topik,
            "ekspresi_avatar": "menyusun",
        }
    return node_retrieve


def buat_node_terapi():
    engine_terapi = EngineTerapi()

    def node_terapi(state: CompanionState) -> CompanionState:
        messages = state.get("messages", [])
        teks = ""
        if messages:
            c = messages[-1].content
            teks = c if isinstance(c, str) else str(c)

        tl = teks.lower()
        teknik = None

        if "panik" in tl or "sesak" in tl:
            teknik = "breathing_478"
        elif "gagal" in tl or "harus" in tl or "semua orang" in tl:
            teknik = "restrukturisasi_kognitif"
        elif "aku tidak berguna" in tl or "capek mikir" in tl:
            teknik = "defusi_act"
        else:
            try:
                hasil = engine_terapi.rekomendasi(teks)
                teknik = hasil.get("teknik")
            except Exception:
                teknik = None

        return {
            "teknik_aktif": teknik,
        }
    return node_terapi


def buat_node_generate(model: BaseChatModel | None = None):
    llm = model or get_chat_model()

    def node_generate(state: CompanionState) -> CompanionState:
        persona = state.get("persona", "netral")
        eskalasi = state.get("eskalasi", "GREEN")
        topik_list = state.get("topik_aktif", [])
        topik = ", ".join(topik_list) if topik_list else None
        ringkasan = state.get("ringkasan_memori", "")
        metadata = state.get("metadata", {})

        system_text = build_system_prompt(
            persona=persona,
            eskalasi=eskalasi,
            topik=topik,
            memori_ringkasan=ringkasan,
            metadata=metadata,
        )

        teknik = state.get("teknik_aktif")
        if teknik:
            system_text += f"\n[Rekomendasi Teknik Klinis]: Selipkan elemen {teknik} secara bersahaja dan menenangkan."

        docs = state.get("dokumen_retrieved", [])
        if docs:
            snippets = " | ".join([d.get("isi", "")[:120] for d in docs if isinstance(d, dict)])
            if snippets:
                system_text += f"\n[Materi Psikoedukasi Terpercaya]: {snippets}"

        chat_input: list[BaseMessage] = [SystemMessage(content=system_text)]
        chat_input.extend(state.get("messages", []))

        try:
            res = llm.invoke(chat_input)
            c = res.content
            if isinstance(c, str):
                draft = c
            elif isinstance(c, list):
                draft = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in c)
            else:
                draft = str(c)
        except Exception as e:
            draft = (
                "Aku di sini mendengarkanmu. Pelan-pelan saja, kita lewati ini satu langkah "
                "demi satu langkah bersama."
            )

        return {
            "respons_draft": draft,
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

    # Tambahkan nodes
    workflow.add_node("safety", evaluasi_keselamatan)
    workflow.add_node("rujuk", node_rujuk_darurat)
    workflow.add_node("retrieve", buat_node_retrieve())
    workflow.add_node("terapi", buat_node_terapi())
    workflow.add_node("generate", buat_node_generate(model=model))
    workflow.add_node("reflection", buat_node_reflection())

    # Set alur eksekusi
    workflow.set_entry_point("safety")
    workflow.add_conditional_edges(
        "safety",
        rute_keselamatan,
        {
            "rujuk": "rujuk",
            "retrieve": "retrieve",
        },
    )
    workflow.add_edge("rujuk", END)
    workflow.add_edge("retrieve", "terapi")
    workflow.add_edge("terapi", "generate")
    workflow.add_edge("generate", "reflection")
    workflow.add_edge("reflection", END)

    if checkpointer is not None:
        return workflow.compile(checkpointer=checkpointer)
    return workflow.compile()
