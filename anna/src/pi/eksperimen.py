# anna/src/pi/eksperimen.py — evaluasi eksperimen jujur (Cohen's d, CI, statistical power, anti p-hacking)
import numpy as np

PRAREGISTRASI = {
    "metric_utama": "skor_beban_mingguan",  # DITULIS SEBELUM DATA DILIHAT
    "ambang_keberhasilan": "d >= 0.2 dengan CI bawah > 0",
    "n_rencana_per_grup": 120,
    "analisis_sekunder": ["retensi_7hr", "jalur_ke_manusia"],
}


def cohen_d_ci(a: np.ndarray, b: np.ndarray) -> dict:
    """Menghitung ukuran efek terstandarisasi Cohen's d beserta interval kepercayaan 95%."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return {"d": 0.0, "CI95": (0.0, 0.0), "berhasil_prareg": False}

    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    if sp == 0:
        return {"d": 0.0, "CI95": (0.0, 0.0), "berhasil_prareg": False}

    d = float((b.mean() - a.mean()) / sp)
    se = float(np.sqrt((na + nb) / (na * nb) + (d ** 2) / (2 * (na + nb))))
    lo, hi = d - 1.96 * se, d + 1.96 * se

    return {
        "d": round(d, 3),
        "CI95": (round(float(lo), 3), round(float(hi), 3)),
        "berhasil_prareg": bool(lo > 0 and d >= 0.2),
    }


def daya_diperlukan(d: float, power: float = 0.8) -> int:
    """Menghitung ukuran sampel minimum yang diperlukan per grup untuk power yang diinginkan."""
    if d <= 0:
        return 999999
    z_a = 1.96
    z_b = {"0.8": 0.84, "0.9": 1.28}.get(str(power), 0.84)
    return int(np.ceil(2 * ((z_a + z_b) / d) ** 2))
