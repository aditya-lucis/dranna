# anna/tests/test_fase5_ekosistem.py — pengujian Fase 5 (Observability, Data Rights, Audit, Localization)
from datetime import datetime, timezone, timedelta
import pytest
from fastapi.testclient import TestClient

from anna.src.api.sse import app
from anna.src.pvi.hotlines import DirektoriHotline, format_rujukan_geo
from anna.src.px.telemetri import TelemetriKlinis
from anna.src.px.audit_pipeline import PipelineAuditKlinis
from anna.src.storage.export_service import ExportService, catat_audit_log
from anna.src.storage.consent_repo import ConsentRepository, ConsentData
from anna.src.storage.mood_repo import MoodRepository
from anna.src.pix.journal import CatatanJurnal


@pytest.fixture
def client():
    return TestClient(app)


def test_hotline_localization_multi_region():
    # 1. Indonesia (ID)
    hl_id = DirektoriHotline.dapatkan_hotline("id")
    assert any("119" in h.nomor for h in hl_id)

    # 2. Malaysia (MY)
    hl_my = DirektoriHotline.dapatkan_hotline("my")
    assert any("15555" in h.nomor for h in hl_my)

    # 3. Singapura (SG)
    hl_sg = DirektoriHotline.dapatkan_hotline("sg")
    assert any("1-767" in h.nomor for h in hl_sg)

    # 4. Global fallback (GL)
    hl_gl = DirektoriHotline.dapatkan_hotline("gl")
    assert any("befrienders" in h.nomor.lower() for h in hl_gl)

    # 5. Rujukan format geo
    rujukan_my = format_rujukan_geo("my", nama_pengguna="Budi")
    assert "Talian HEAL" in rujukan_my
    assert "Budi" in rujukan_my


def test_telemetri_prometheus_format():
    t = TelemetriKlinis()
    t.catat_request(durasi_ms=120.5, eskalasi="GREEN")
    t.catat_request(durasi_ms=180.0, eskalasi="YELLOW")
    t.catat_request(durasi_ms=95.0, eskalasi="RED")
    
    prom_text = t.format_prometheus()
    assert "anna_requests_total 3" in prom_text
    assert "anna_crisis_red_total 1" in prom_text
    assert "# TYPE anna_latency_p95_ms gauge" in prom_text


def test_export_service_and_ttl_pruning(tmp_path):
    db_file = tmp_path / "test_ecosystem.db"
    exp_srv = ExportService(db_path=db_file)
    c_repo = ConsentRepository(db_path=db_file)
    m_repo = MoodRepository(db_path=db_file)
    u_id = "user-eco-1"

    # Set consent dengan TTL 30 hari
    c_repo.simpan_consent(ConsentData(user_id=u_id, durasi_simpan_hari=30))

    # Catatan mood baru (hari ini)
    m_repo.simpan_catatan(
        u_id,
        CatatanJurnal(
            id="m-today",
            waktu_iso=datetime.now(timezone.utc).isoformat(),
            mood_skor=0.7,
            energi_skor=0.8,
            catatan_refleksi="Sangat produktif",
        )
    )

    # Catatan mood usang (45 hari yang lalu, melewati TTL 30 hari)
    old_time = (datetime.now(timezone.utc) - timedelta(days=45)).isoformat()
    m_repo.simpan_catatan(
        u_id,
        CatatanJurnal(
            id="m-old",
            waktu_iso=old_time,
            mood_skor=0.1,
            energi_skor=0.2,
            catatan_refleksi="Catatan lama",
        )
    )

    # 1. Ekspor data lengkap
    paket = exp_srv.ekspor_data_pengguna(u_id)
    assert paket["user_id"] == u_id
    assert "UU PDP" in paket["standar_kepatuhan"]
    assert len(paket["catatan_mood_jurnal"]) == 2

    # 2. Eksekusi TTL Pruning
    laporan_prune = exp_srv.bersihkan_data_kedaluwarsa(u_id)
    assert laporan_prune["mood_logs"] == 1  # 1 entri lama terhapus

    # 3. Verifikasi sisa entri
    sisa = m_repo.ambil_riwayat(u_id)
    assert len(sisa) == 1
    assert sisa[0].id == "m-today"


def test_clinical_audit_release_pipeline():
    laporan = PipelineAuditKlinis.jalankan_audit_penuh()
    assert laporan.siap_produksi is True
    assert laporan.zero_fn_terpenuhi is True
    assert laporan.keputusan == "GO"
    assert laporan.skor_benchmark_klinis >= 4.0


def test_api_fase5_endpoints(client):
    u_id = "test-api-f5"

    # 1. Metrics Endpoint
    resp_metrics = client.get("/metrics")
    assert resp_metrics.status_code == 200
    assert "anna_requests_total" in resp_metrics.text

    # 2. Export Endpoint
    resp_exp = client.get(f"/api/v1/user/{u_id}/export")
    assert resp_exp.status_code == 200
    assert resp_exp.json()["user_id"] == u_id
    assert "persetujuan_privasi" in resp_exp.json()

    # 3. Prune Endpoint (mendukung durasi_hari dan rincian response)
    resp_prune = client.post(f"/api/v1/user/{u_id}/prune?durasi_hari=15")
    assert resp_prune.status_code == 200
    assert "laporan_pembersihan" in resp_prune.json()
    assert "rincian" in resp_prune.json()

    # 4. Audit Report Endpoint
    resp_audit = client.get("/api/v1/audit/report")
    assert resp_audit.status_code == 200
    assert resp_audit.json()["keputusan"] == "GO"


def test_ttl_pruning_fallback_when_user_not_in_consent_ledger(tmp_path):
    db_file = tmp_path / "test_fallback_prune.db"
    exp_srv = ExportService(db_path=db_file)
    m_repo = MoodRepository(db_path=db_file)
    u_id = "user-tanpa-consent"

    # User belum ada di consent ledger, tapi punya catatan usang 100 hari lalu
    old_time = (datetime.now(timezone.utc) - timedelta(days=100)).isoformat()
    m_repo.simpan_catatan(
        u_id,
        CatatanJurnal(
            id="m-old-orphan",
            waktu_iso=old_time,
            mood_skor=0.2,
            energi_skor=0.3,
            catatan_refleksi="Data lama tanpa consent custom",
        ),
    )

    # Pruning harus menggunakan fallback default 90 hari dan berhasil menghapus record lama
    laporan = exp_srv.bersihkan_data_kedaluwarsa(user_id=u_id)
    assert laporan["mood_logs"] == 1

    sisa = m_repo.ambil_riwayat(u_id)
    assert len(sisa) == 0

