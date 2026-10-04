# anna/src/pi/deskriptif.py — ringkasan mood mingguan yang jujur
import numpy as np


def ringkasan_mood(x: np.ndarray, n_hilang: int = 0) -> dict:
    """x: skor mood harian (-1.0 s/d 1.0); n_hilang: hari tanpa entri jurnal."""
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return {
            "n": 0,
            "n_hilang": n_hilang,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "iqr": 0.0,
            "min": 0.0,
            "max": 0.0,
            "datar_flat": False,
        }

    q1, q2, q3 = np.percentile(x, [25, 50, 75])
    std_val = float(x.std(ddof=1)) if x.size > 1 else 0.0
    return {
        "n": int(x.size),
        "n_hilang": n_hilang,
        "mean": round(float(x.mean()), 3),
        "median": round(float(q2), 3),
        "std": round(std_val, 3),
        "iqr": round(float(q3 - q1), 3),
        "min": round(float(x.min()), 3),
        "max": round(float(x.max()), 3),
        "datar_flat": bool(std_val < 0.08) if x.size > 3 else False,
    }


if __name__ == "__main__":
    w1 = np.array([0.1, 0.0, -0.9, -0.8, 0.1, 0.2, 0.1])
    w2 = np.array([-0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2])
    print("minggu 1 (distribusi miring):", ringkasan_mood(w1))
    print("minggu 2 (datar / mati rasa):", ringkasan_mood(w2))
