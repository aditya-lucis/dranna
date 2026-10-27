# anna/src/px/healthz.py — endpoint liveness, readiness probe & status klinis
"""
Health Check & Readiness Probes (Bab 131):
- /healthz: Liveness probe (memverifikasi proses berjalan)
- /readyz: Readiness probe (memverifikasi kesiapan korpus, guardrail, & model)
- /status/klinis: Laporan kesehatan emosional & telemetri sistem
"""
import time
from fastapi import APIRouter, Response, status
from anna.src.pvi.tangga import TanggaRisiko
from anna.src.pvi.guardrails import GuardrailKrisis
from anna.src.px.telemetri import TelemetriKlinis

router_healthz = APIRouter(tags=["Health & Telemetri"])
_telemetri_global = TelemetriKlinis()


def cek_kesiapan_sistem() -> dict:
    """Memeriksa integritas seluruh komponen subsistem sebelum menerima trafik produksi."""
    subsistem = {}

    # 1. Uji Tangga Risiko
    try:
        t = TanggaRisiko()
        res = t.evaluasi("halo")
        subsistem["tangga_risiko"] = "OK" if res.level is not None else "ERROR"
    except Exception as e:
        subsistem["tangga_risiko"] = f"ERROR: {str(e)}"

    # 2. Uji Guardrails Krisis
    try:
        g = GuardrailKrisis()
        res = g.periksa("halo")
        subsistem["guardrails"] = "OK" if res["aman"] is True else "ERROR"
    except Exception as e:
        subsistem["guardrails"] = f"ERROR: {str(e)}"

    semua_ok = all(v == "OK" for v in subsistem.values())
    return {
        "siap": semua_ok,
        "subsistem": subsistem,
        "waktu": time.time(),
    }


@router_healthz.get("/healthz")
def liveness_probe():
    """Liveness probe standar Kubernetes / Docker: aplikasi hidup."""
    return {"status": "alive", "timestamp": time.time()}


@router_healthz.get("/readyz")
def readiness_probe(response: Response):
    """Readiness probe: aplikasi siap melayani percakapan."""
    hasil = cek_kesiapan_sistem()
    if not hasil["siap"]:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return hasil


@router_healthz.get("/status/klinis")
def status_klinis():
    """Menyajikan ringkasan metrik telemetri performa dan penanganan krisis."""
    return _telemetri_global.ringkasan()


@router_healthz.get("/metrics")
def prometheus_metrics():
    """Ekspor metrik berformat Prometheus untuk Prometheus scraper."""
    teks = _telemetri_global.format_prometheus()
    return Response(content=teks, media_type="text/plain; version=0.0.4")
