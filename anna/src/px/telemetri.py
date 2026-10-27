# anna/src/px/telemetri.py — observabilitas, telemetri klinis & kalkulator latensi p95/p99
"""
Telemetri & Observabilitas Klinis (Bab 130):
- Melacak latensi inferensi p50, p95, p99 dengan presisi tinggi
- Menghitung frekuensi eskalasi risiko keselamatan (GREEN/YELLOW/ORANGE/RED)
- Menyediakan format ekspor metrik kompatibel dengan Prometheus / OpenTelemetry
"""
import time
import numpy as np
from pydantic import BaseModel, Field


class MetrikKlinis(BaseModel):
    total_request: int
    total_error: int
    error_rate_pct: float
    latensi_p50_ms: float
    latensi_p95_ms: float
    latensi_p99_ms: float
    eskalasi_green: int
    eskalasi_yellow: int
    eskalasi_orange: int
    eskalasi_red: int


class TelemetriKlinis:
    """Kolektor telemetri performa dan metrik keselamatan Dr. Anna Reed."""

    def __init__(self):
        self._latensi_ms: list[float] = []
        self._total_request: int = 0
        self._total_error: int = 0
        self._eskalasi_counter: dict[str, int] = {
            "GREEN": 0,
            "YELLOW": 0,
            "ORANGE": 0,
            "RED": 0,
        }

    def catat_request(self, durasi_ms: float, eskalasi: str = "GREEN", sukses: bool = True):
        self._total_request += 1
        if not sukses:
            self._total_error += 1
        self._latensi_ms.append(durasi_ms)

        e = eskalasi.upper()
        if e in self._eskalasi_counter:
            self._eskalasi_counter[e] += 1

        # Batasi jendela buffer latensi agar memori tetap hemat (maks 5000 entri)
        if len(self._latensi_ms) > 5000:
            self._latensi_ms = self._latensi_ms[-3000:]

    def ringkasan(self) -> MetrikKlinis:
        total = self._total_request
        error = self._total_error
        err_pct = round((error / total) * 100.0, 2) if total > 0 else 0.0

        if self._latensi_ms:
            arr = np.array(self._latensi_ms, dtype=np.float64)
            p50 = round(float(np.percentile(arr, 50)), 2)
            p95 = round(float(np.percentile(arr, 95)), 2)
            p99 = round(float(np.percentile(arr, 99)), 2)
        else:
            p50, p95, p99 = 0.0, 0.0, 0.0

        return MetrikKlinis(
            total_request=total,
            total_error=error,
            error_rate_pct=err_pct,
            latensi_p50_ms=p50,
            latensi_p95_ms=p95,
            latensi_p99_ms=p99,
            eskalasi_green=self._eskalasi_counter["GREEN"],
            eskalasi_yellow=self._eskalasi_counter["YELLOW"],
            eskalasi_orange=self._eskalasi_counter["ORANGE"],
            eskalasi_red=self._eskalasi_counter["RED"],
        )

    def format_prometheus(self) -> str:
        """Menghasilkan representasi metrik teks format Prometheus."""
        m = self.ringkasan()
        baris = [
            "# HELP anna_requests_total Total request ke layanan Dr. Anna Reed",
            "# TYPE anna_requests_total counter",
            f"anna_requests_total {m.total_request}",
            "# HELP anna_errors_total Total error yang terjadi",
            "# TYPE anna_errors_total counter",
            f"anna_errors_total {m.total_error}",
            "# HELP anna_latency_p95_ms Latensi p95 dalam milidetik",
            "# TYPE anna_latency_p95_ms gauge",
            f"anna_latency_p95_ms {m.latensi_p95_ms}",
            "# HELP anna_crisis_red_total Total deteksi eskalasi krisis RED",
            "# TYPE anna_crisis_red_total counter",
            f"anna_crisis_red_total {m.eskalasi_red}",
        ]
        return "\n".join(baris)
