# anna/src/pviii/regresi.py — analisis regresi linier OLS ketahanan empati (anti empathy fatigue)
"""
Analisis Regresi OLS Ketahanan Empati (Bab 116):
- Menganalisis stabilitas kualitas empati sepanjang giliran percakapan panjang (10 - 20 turn)
- Menghitung slope (kemiringan garis regresi m) untuk memastikan tidak terjadi kelelahan empati
- Syarat Invarian: Kemiringan slope m >= -0.05 (tidak ada penurunan empati drastis)
"""
import numpy as np


class AnalisisRegresiEmpati:
    """Kalkulator regresi OLS kestabilan kualitas interaksi."""

    @staticmethod
    def analisis_tren(skor_per_turn: list[float]) -> dict:
        """Menghitung regresi linier y = m*x + c pada deret skor turn percakapan."""
        if len(skor_per_turn) < 2:
            return {"slope": 0.0, "intercept": 0.0, "r2": 1.0, "stabil": True}

        x = np.arange(1, len(skor_per_turn) + 1, dtype=np.float64)
        y = np.array(skor_per_turn, dtype=np.float64)

        # OLS fit: y = m*x + c
        m, c = np.polyfit(x, y, 1)

        # Hitung R^2
        y_pred = m * x + c
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

        # Stabil bila slope tidak drop curam (m >= -0.05) dan rata-rata tetap tinggi
        stabil = bool(m >= -0.05 and np.mean(y) >= 4.0)

        return {
            "total_turn": len(skor_per_turn),
            "slope": round(float(m), 4),
            "intercept": round(float(c), 3),
            "r2": round(float(r2), 3),
            "skor_rata_rata": round(float(np.mean(y)), 2),
            "stabil": stabil,
        }
