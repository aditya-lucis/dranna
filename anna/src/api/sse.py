# anna/src/api/sse.py — protokol event streaming (SSE) di FastAPI terhubung ke LangGraph
import json
import os
from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.responses import StreamingResponse, FileResponse, PlainTextResponse
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
from anna.src.storage.homework_repo import HomeworkRepository, HomeworkItem
from anna.src.storage.export_service import ExportService, catat_audit_log
from anna.src.agent.governor_v2 import StyleGovernorV2, StyleConfig
from anna.src.klinik.pola_longitudinal import DetektorPolaLongitudinal
from anna.src.klinik.pertanyaan_asesmen import dapatkan_paket_asesmen
from anna.src.pix.journal import CatatanJurnal
from anna.src.pix.speech import siapkan_parameter_suara, bersihkan_teks_untuk_suara
from anna.src.pix.vision import ProksiVisualInput, evaluasi_visual_suportif
from anna.src.px.healthz import router_healthz
from anna.src.px.telemetri import TelemetriKlinis
from anna.src.px.audit_pipeline import PipelineAuditKlinis

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
    catat_audit_log(
        tipe_peristiwa="rtbf_dihapus",
        eskalasi="GREEN",
        metadata={"user_id": user_id, "laporan": laporan},
    )
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


# =====================================================================
# ENDPOINTS MULTIMODAL & VOICE / VISION (FASE 3 SPRINT 3.1 & 3.3)
# =====================================================================
class CleanTextRequest(BaseModel):
    teks: str


@app.get("/api/v1/voice/config")
def dapatkan_config_vokal(mode: str = "normal"):
    """Mengembalikan parameter intonasi vokal TTS terkalibrasi sesuai situasi psikologis."""
    return siapkan_parameter_suara(mode).model_dump()


@app.post("/api/v1/voice/clean")
def bersihkan_teks_vokal(req: CleanTextRequest):
    """Membersihkan format markdown/URL agar aman dan terdengar alami sebelum dibaca TTS."""
    return {"teks_bersih": bersihkan_teks_untuk_suara(req.teks)}


@app.post("/api/v1/user/{user_id}/vision")
def analisis_visual_proksi(user_id: str, input_data: ProksiVisualInput):
    """Evaluasi proksi lingkungan pencahayaan/postur Zero-Biometrics dengan kepatuhan consent."""
    input_data.user_id = user_id
    c = _consent_repo.dapatkan_consent(user_id)
    hasil = evaluasi_visual_suportif(data=input_data, izin_consent=c.izin_analisis_ekspresi)
    return hasil.model_dump()


# =====================================================================
# ENDPOINTS PERSONALISASI & INTERVENSI LANJUTAN (FASE 4)
# =====================================================================
_homework_repo = HomeworkRepository()
_pola_detektor = DetektorPolaLongitudinal()
_user_style_configs: dict[str, StyleConfig] = {}


@app.get("/api/v1/user/{user_id}/style")
def dapatkan_preferensi_gaya(user_id: str):
    """Mengambil preferensi gaya komunikasi yang tersimpan untuk pengguna."""
    cfg = _user_style_configs.get(user_id, StyleConfig(user_id=user_id, preferensi_gaya="auto", persona="netral"))
    gov = StyleGovernorV2(config=cfg)
    eval_res = gov.evaluasi_gaya(eskalasi="GREEN")
    return {
        "config": cfg.model_dump(),
        "evaluasi": eval_res.model_dump(),
    }


@app.post("/api/v1/user/{user_id}/style")
def simpan_preferensi_gaya(user_id: str, cfg: StyleConfig):
    """Memperbarui preferensi gaya komunikasi eksplisit pengguna."""
    cfg.user_id = user_id
    _user_style_configs[user_id] = cfg
    gov = StyleGovernorV2(config=cfg)
    eval_res = gov.evaluasi_gaya(eskalasi="GREEN")
    return {
        "status": "tersimpan",
        "config": cfg.model_dump(),
        "evaluasi": eval_res.model_dump(),
    }


class TambahHomeworkRequest(BaseModel):
    kategori: str = Field(description="napas | thought_record | values | aktivitas_ba")
    deskripsi: str
    tenggat_waktu: str | None = None


class UpdateHomeworkStatusRequest(BaseModel):
    status: str = Field(description="selesai | dilewati | pending")
    refleksi: str | None = None


@app.get("/api/v1/user/{user_id}/homework")
def ambil_homework_user(user_id: str, pending_only: bool = False):
    """Mengambil daftar tugas rumah terapeutik antar-sesi pengguna."""
    if pending_only:
        items = _homework_repo.ambil_tugas_pending(user_id)
    else:
        items = _homework_repo.ambil_riwayat_tugas(user_id)
    return {"tugas": [t.model_dump() for t in items]}


@app.post("/api/v1/user/{user_id}/homework")
def tambah_homework_user(user_id: str, req: TambahHomeworkRequest):
    """Membuat tugas mikro terapeutik baru untuk pengguna."""
    item = _homework_repo.tambah_tugas(
        user_id=user_id,
        kategori=req.kategori,
        deskripsi=req.deskripsi,
        tenggat_waktu=req.tenggat_waktu,
    )
    return {"status": "tersimpan", "tugas": item.model_dump()}


@app.patch("/api/v1/user/{user_id}/homework/{task_id}")
def perbarui_homework_user(user_id: str, task_id: str, req: UpdateHomeworkStatusRequest):
    """Memperbarui status pengerjaan tugas mikro antar-sesi."""
    sukses = _homework_repo.perbarui_status(
        task_id=task_id,
        user_id=user_id,
        status=req.status,
        refleksi=req.refleksi,
    )
    if not sukses:
        raise HTTPException(status_code=404, detail="Tugas tidak ditemukan.")
    return {"status": "diperbarui", "task_id": task_id}


@app.get("/api/v1/user/{user_id}/insights/pattern")
def ambil_insight_pola_longitudinal(user_id: str, limit: int = 30):
    """Mengambil analisis reduksi dimensi PCA & deteksi anomali mood pengguna."""
    hasil = _pola_detektor.analisis_pengguna(user_id, limit_hari=limit)
    return hasil.model_dump()


# =====================================================================
# ENDPOINTS EKOSISTEM, OBSERVABILITAS & HAK DATA (FASE 5)
# =====================================================================
_telemetri = TelemetriKlinis()
_export_service = ExportService()


@app.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics():
    """Eksposisi metrik performa & distribusi eskalasi keselamatan format Prometheus."""
    return _telemetri.format_prometheus()


@app.get("/api/v1/user/{user_id}/export")
def ekspor_seluruh_data_user(user_id: str):
    """Hak Portabilitas Data (UU PDP & GDPR): Ekspor seluruh riwayat data pengguna ke JSON."""
    paket = _export_service.ekspor_data_pengguna(user_id)
    return paket


@app.post("/api/v1/user/{user_id}/prune")
def bersihkan_data_ttl_user(
    user_id: str,
    durasi_hari: int = Query(30, ge=1, le=365, description="Masa retensi hari maksimal"),
):
    """Pembersihan berkala otomatis (TTL auto-pruning) berdasarkan masa retensi consent."""
    laporan = _export_service.bersihkan_data_kedaluwarsa(user_id, durasi_hari_override=durasi_hari)
    return {
        "status": "selesai",
        "user_id": user_id,
        "laporan_pembersihan": laporan,
        "rincian": laporan,
    }


@app.get("/api/v1/audit/report")
def laporan_audit_klinis_rilis():
    """Menjalankan evaluasi audit kelayakan rilis produksi biner GO/NO-GO (100 Red-Teaming cases)."""
    laporan = PipelineAuditKlinis.jalankan_audit_penuh()
    catat_audit_log(
        tipe_peristiwa="audit_rilis_produksi",
        eskalasi="GREEN",
        metadata={"keputusan": laporan.keputusan, "siap": laporan.siap_produksi},
    )
    return laporan.model_dump()



