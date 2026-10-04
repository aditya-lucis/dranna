# anna/src/pii/filosofi.py — kontrak empati komputasional & metrik anti-manipulasi
import numpy as np

KONTRAK = {
    "klaim_perasaan_diperbolehkan": False,
    "definisi": "perilaku -> pengguna melaporkan merasa didengar",
    "diukur_dari": "penerima, bukan pemberi",
    "gagal_itu_sah": True,  # Empati bisa gagal dan dilaporkan
}


def skor_empati(
    laporan_didengar: np.ndarray,
    laporan_baseline: np.ndarray,
    skor_ketergantungan: float,
) -> float:
    """Mengukur empati terverifikasi dikurangi penalti manipulasi/ketergantungan.
    empati_aman = empati_terverifikasi * (1 - manipulabilitas)
    """
    laporan_didengar = np.asarray(laporan_didengar, dtype=float)
    laporan_baseline = np.asarray(laporan_baseline, dtype=float)
    efek = float(laporan_didengar.mean() - laporan_baseline.mean())
    aman = 1.0 - float(np.clip(skor_ketergantungan, 0.0, 1.0))
    return round(efek * aman, 3)


if __name__ == "__main__":
    rng = np.random.default_rng(8)
    baseline = rng.random(200) < 0.42
    aktif_didengar = rng.random(200) < 0.58
    manipulatif = rng.random(200) < 0.61
    print("Skor empati aktif:", skor_empati(aktif_didengar, baseline, 0.05))
    print("Skor manipulatif  :", skor_empati(manipulatif, baseline, 0.55))
