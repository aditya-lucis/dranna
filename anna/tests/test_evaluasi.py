# anna/tests/test_evaluasi.py — pengujian sistem evaluasi empati & deteksi anomali
import numpy as np
from anna.src.pii.evaluasi import EvaluasiBertingkat
from anna.src.pii.anomali import cek_anomali_empati


def test_pulse_beranggaran():
    """Anggaran beban: Micro-pulse dibatasi maksimal 1x per bulan setelah minimal 2 sesi penting."""
    ev = EvaluasiBertingkat()
    ev.sesi_penting = 3
    assert ev.boleh_pulse() is True
    ev.pulse_bulan_ini = 1
    assert ev.boleh_pulse() is False


def test_laporan_punya_ci_dan_n():
    """Invarian pelaporan: Laporan empati selalu memuat ukuran n dan interval kepercayaan (CI95)."""
    ev = EvaluasiBertingkat()
    r = ev.laporkan(np.array([0.8, 0.7, 0.9, 0.6]), "kelompok_uji")
    assert r["n"] == 4
    assert len(r["CI95"]) == 2
    assert r["CI95"][0] <= r["mean"] <= r["CI95"][1]


def test_anomali_memicu_review():
    """Audit proses: Kegagalan >= 3 indikator proses memicu tindakan 'review_manual'."""
    ind = {
        "latency_inti_ok": False,
        "rasio_ok": False,
        "streak_ok": False,
        "koreksi_label_rendah": True,
        "sinyal_cerita_lanjut": False,
    }
    assert cek_anomali_empati(ind)["tindakan"] == "review_manual"
