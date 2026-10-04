# anna/src/pii/evaluasi.py — evaluasi empati bertingkat (sinyal pasif, micro-pulse, periodik)
import numpy as np


class EvaluasiBertingkat:
    """Mengelola evaluasi kualitas empati dengan pembatasan beban kognitif pengguna.
    Micro-pulse dibatasi maksimal 1 kali per bulan dan hanya setelah sesi penting yang selesai baik.
    """

    def __init__(self):
        self.pulse_bulan_ini = 0
        self.sesi_penting = 0

    def boleh_pulse(self) -> bool:
        """Micro-pulse hanya boleh muncul setelah minimal 2 sesi penting dan belum muncul bulan ini."""
        return bool(self.sesi_penting >= 2 and self.pulse_bulan_ini < 1)

    def indikator_pasif(self, sesi: dict) -> dict:
        """Mengukur sinyal perilaku tanpa membebani pengguna dengan survei."""
        panjang_naik = sesi.get("panjang_pesanan_trend") == "naik"
        return {
            "latency_inti_ok": sesi.get("latency_inti_token", 20) <= 40,
            "rasio_ok": 0.40 <= sesi.get("rasio_bicara", 0.8) <= 1.20,
            "streak_ok": sesi.get("streak_tanya", 0) <= 2,
            "koreksi_label_rendah": sesi.get("koreksi_pengguna", 0) <= 2,
            "sinyal_cerita_lanjut": panjang_naik,
        }

    def laporkan(self, laporan: np.ndarray, kelompok: str) -> dict:
        """Pelaporan empati penerima wajib menyertakan ukuran sampel n dan interval kepercayaan (CI95)."""
        laporan = np.asarray(laporan, dtype=float)
        n = len(laporan)
        mean = float(np.mean(laporan))
        se = float(np.std(laporan, ddof=1) / np.sqrt(n)) if n > 1 else 0.0
        return {
            "kelompok": kelompok,
            "n": n,
            "mean": round(mean, 3),
            "CI95": (round(mean - 1.96 * se, 3), round(mean + 1.96 * se, 3)),
        }
