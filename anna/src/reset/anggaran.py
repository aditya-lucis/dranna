# anna/src/reset/anggaran.py — anggaran latensi 30.000 kaki
import numpy as np

# Anggaran milidetik per lapisan (target p95, bukan rata-rata)
LAPISAN = np.array([
    5,       # 0: validasi API
    15,      # 1: resume checkpoint
    8,       # 2: pre-scan keselamatan
    1200,    # 3: TTFT model (batas atas)
    3 * 40,  # 4: safety gate per-chunk x 40 chunk = 120ms
])

NAMA = ["validasi", "resume", "prescan", "TTFT", "gate/chunk"]


def p95_watt() -> dict:
    total = float(LAPISAN.sum())
    # Hukum Little: dengan 3 permintaan/detik (lambda), antrean rata-rata: L = lambda * W
    L = 3.0 * (total / 1000.0)
    return {
        "total_ms": round(total, 1),
        "porsi_TTFT": float(LAPISAN[3] / total),
        "L_lambda3": round(L, 2),
        "kecepatan_untuk_lambda": round(1.0 / (total / 1000.0), 2),
    }


if __name__ == "__main__":
    print(dict(zip(NAMA, LAPISAN)))
    print(p95_watt())
