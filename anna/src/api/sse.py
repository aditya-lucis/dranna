# anna/src/api/sse.py — protokol event streaming (SSE) di FastAPI terhubung ke LangGraph
import json
import os
from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from anna.src.agent.streaming import stream_companion
from anna.src.agent.checkpoint import get_default_checkpointer
from anna.src.agent.graph import create_companion_graph
from anna.src.storage.consent_repo import ConsentRepository, ConsentData
from anna.src.storage.mood_repo import MoodRepository
from anna.src.storage.asesmen_repo import AsesmenRepository, AsesmenSubmit
from anna.src.storage.safety_plan_repo import SafetyPlanRepository, SafetyPlanModel
from anna.src.storage.episodic_repo import EpisodicRepository
from anna.src.klinik.pertanyaan_asesmen import dapatkan_paket_asesmen
from anna.src.pix.journal import CatatanJurnal
from anna.src.px.healthz import router_healthz

app = FastAPI(title="Project Serenity SSE API", version="1.0.0")
app.include_router(router_healthz)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
WEB_DIR = os.path.join(ROOT_DIR, "web")

if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


@app.get("/", response_class=FileResponse)
def index_page():
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Dr. Anna Reed API active. Go to /docs for API documentation."}


@app.get("/manifest.json", response_class=FileResponse)
def pwa_manifest():
    manifest_path = os.path.join(WEB_DIR, "public", "manifest.json")
    if os.path.exists(manifest_path):
        return FileResponse(manifest_path, media_type="application/manifest+json")
    return {}

# Checkpointer singleton untuk sesi
_checkpointer = get_default_checkpointer()
_graph = create_companion_graph(checkpointer=_checkpointer)


class ChatStreamRequest(BaseModel):
    pesan: str = Field(..., min_length=1, max_length=2000)
    persona: str = Field("netral", pattern="^(netral|waifu|sister)$")
    geo: str = Field("id", max_length=5)
    jam: int | None = Field(None, ge=0, le=23, description="Jam lokal pengguna (0-23)")
    item9_flag: bool = Field(False, description="Flag item-9 PHQ-9 positif")


@app.get("/api/v1/sesi/{sesi_id}/stream")
async def stream_get(
    sesi_id: str,
    pesan: str = Query("Halo Anna", description="Pesan dari pengguna"),
    persona: str = Query("netral", description="Persona: netral | waifu | sister"),
    geo: str = Query("id", description="Kode wilayah"),
    jam: int | None = Query(None, ge=0, le=23, description="Jam lokal pengguna (0-23)"),
    item9: bool = Query(False, description="Flag item-9 PHQ-9 positif"),
):
    """Streaming respons LangGraph Dr. Anna Reed via Server-Sent Events (GET)."""
    return StreamingResponse(
        stream_companion(
            pesan_pengguna=pesan,
            sesi_id=sesi_id,
            persona=persona,
            graph=_graph,
            jam=jam,
            item9_flag=item9,
            geo=geo,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/v1/sesi/{sesi_id}/stream")
async def stream_post(
    sesi_id: str,
    req: ChatStreamRequest,
):
    """Streaming respons LangGraph Dr. Anna Reed via Server-Sent Events (POST)."""
    return StreamingResponse(
        stream_companion(
            pesan_pengguna=req.pesan,
            sesi_id=sesi_id,
            persona=req.persona,
            graph=_graph,
            jam=req.jam,
            item9_flag=req.item9_flag,
            geo=req.geo,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# =====================================================================
# ENDPOINTS KENDALI DATA & CONSENT (FASE 2 SPRINT 2.1)
# =====================================================================
_consent_repo = ConsentRepository()


@app.get("/api/v1/user/{user_id}/consent")
def dapatkan_consent_user(user_id: str):
    """Mengambil status 5-komponen persetujuan privasi pengguna."""
    return _consent_repo.dapatkan_consent(user_id)


@app.post("/api/v1/user/{user_id}/consent")
def perbarui_consent_user(user_id: str, consent: ConsentData):
    """Memperbarui pengaturan persetujuan privasi pengguna."""
    consent.user_id = user_id
    return _consent_repo.simpan_consent(consent)


@app.delete("/api/v1/user/{user_id}/data")
def lupakan_data_user(user_id: str):
    """Right to be Forgotten: Menghapus seluruh data, catatan, dan memori pengguna."""
    laporan = _consent_repo.hapus_seluruh_data_user(user_id)
    # Hapus thread pada checkpointer jika didukung
    if hasattr(_checkpointer, "delete_thread"):
        try:
            _checkpointer.delete_thread(user_id)
        except Exception:
            pass
    return {
        "status": "terhapus",
        "pesan": "Seluruh riwayat, memori episodik, catatan mood, dan asesmen berhasil dihapus permanen.",
        "laporan": laporan,
    }


# =====================================================================
# ENDPOINTS JURNAL MOOD & DETEKSI FLATLINE (FASE 2 SPRINT 2.2)
# =====================================================================
_mood_repo = MoodRepository()


@app.get("/api/v1/user/{user_id}/journal")
def ambil_jurnal_user(user_id: str, limit: int = 14):
    """Mengambil riwayat catatan mood pengguna dan analisis flatline 7-hari."""
    riwayat = _mood_repo.ambil_riwayat(user_id, limit=limit)
    analisis = _mood_repo.analisis_flatline(user_id, ambang_hari=7)
    return {
        "riwayat": [c.model_dump() for c in riwayat],
        "analisis": analisis.model_dump(),
    }


@app.post("/api/v1/user/{user_id}/journal")
def simpan_jurnal_user(user_id: str, catatan: CatatanJurnal):
    """Menyimpan entri mood harian baru dan mengembalikan evaluasi tren terbaru."""
    hasil = _mood_repo.simpan_catatan(user_id, catatan)
    analisis = _mood_repo.analisis_flatline(user_id, ambang_hari=7)
    return {
        "status": "tersimpan",
        "catatan": hasil.model_dump(),
        "analisis": analisis.model_dump(),
    }


# =====================================================================
# ENDPOINTS ASESMEN KLINIS INTERAKTIF (FASE 2 SPRINT 2.3)
# =====================================================================
_asesmen_repo = AsesmenRepository()


@app.get("/api/v1/asesmen/pertanyaan/{jenis}")
def ambil_pertanyaan_asesmen(jenis: str):
    """Mengambil butir pertanyaan & skala instrumen klinis (PHQ-9 / GAD-7)."""
    try:
        return dapatkan_paket_asesmen(jenis)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/user/{user_id}/asesmen")
def kirim_jawaban_asesmen(user_id: str, submit: AsesmenSubmit):
    """Memproses jawaban asesmen, mengevaluasi Item-9, dan menyimpan skor non-diagnostik."""
    record = _asesmen_repo.proses_dan_simpan(user_id, submit)
    return record.model_dump()


@app.get("/api/v1/user/{user_id}/asesmen")
def ambil_riwayat_asesmen_user(user_id: str, limit: int = 10):
    """Mengambil riwayat asesmen klinis yang pernah dikerjakan pengguna."""
    riwayat = _asesmen_repo.ambil_riwayat(user_id, limit=limit)
    return {
        "riwayat": [r.model_dump() for r in riwayat],
    }


# =====================================================================
# ENDPOINTS SAFETY PLAN & MEMORI EPISODIK (FASE 2 SPRINT 2.4)
# =====================================================================
_safety_repo = SafetyPlanRepository()
_episodic_repo = EpisodicRepository()


@app.get("/api/v1/user/{user_id}/safety-plan")
def dapatkan_safety_plan(user_id: str, geo: str = "id"):
    """Mengambil draf Safety Plan Stanley-Brown pengguna."""
    return _safety_repo.ambil_safety_plan(user_id, geo=geo).model_dump()


@app.post("/api/v1/user/{user_id}/safety-plan")
def perbarui_safety_plan(user_id: str, plan: SafetyPlanModel):
    """Memperbarui draf Safety Plan pengguna."""
    plan.user_id = user_id
    saved = _safety_repo.simpan_safety_plan(plan)
    return saved.model_dump()


class RecordMemoryInput(BaseModel):
    sesi_id: str
    topik: str
    ringkasan: str
    valence: float = 0.0
    teknik: str | None = None


@app.get("/api/v1/user/{user_id}/memory")
def ambil_memori_user(user_id: str, limit: int = 5):
    """Mengambil riwayat ringkasan memori episodik Zero-PII pengguna."""
    memori = _episodic_repo.ambil_memori_terbaru(user_id, limit=limit)
    return {"memori": [m.model_dump() for m in memori]}


@app.post("/api/v1/user/{user_id}/memory")
def catat_memori_user(user_id: str, data: RecordMemoryInput):
    """Mencatat ringkasan sesi ke memori episodik dengan redaksi PII otomatis."""
    # Pastikan pengguna memberi izin simpan riwayat
    c = _consent_repo.dapatkan_consent(user_id)
    if not c.izin_simpan_riwayat:
        return {"status": "diabaikan", "pesan": "Pengguna tidak memberikan izin simpan riwayat."}

    hasil = _episodic_repo.simpan_memori(
        user_id=user_id,
        sesi_id=data.sesi_id,
        topik=data.topik,
        ringkasan=data.ringkasan,
        valence=data.valence,
        teknik=data.teknik,
    )
    return {"status": "tersimpan", "memori": hasil.model_dump()}
