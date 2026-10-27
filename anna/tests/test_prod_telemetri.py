# anna/tests/test_prod_telemetri.py — Unit test telemetri & metrik latensi
import pytest
from anna.src.px.telemetri import TelemetriKlinis


def test_telemetri_pencatatan_dan_persentil():
    telem = TelemetriKlinis()
    durasi_list = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
    for d in durasi_list:
        telem.catat_request(durasi_ms=d, eskalasi="GREEN", sukses=True)

    m = telem.ringkasan()
    assert m.total_request == 10
    assert 45.0 <= m.latensi_p50_ms <= 65.0
    assert m.latensi_p95_ms >= m.latensi_p50_ms
    assert m.latensi_p99_ms >= m.latensi_p95_ms
    assert m.eskalasi_green == 10


def test_telemetri_format_prometheus():
    telem = TelemetriKlinis()
    telem.catat_request(durasi_ms=50.0, eskalasi="RED", sukses=True)
    prom = telem.format_prometheus()

    assert "anna_requests_total 1" in prom
    assert "anna_crisis_red_total 1" in prom
    assert "anna_latency_p95_ms 50.0" in prom
