# anna/src/pi/attention.py — mini scaled dot-product attention & entropi fokus
import numpy as np


def softmax_stabil(z: np.ndarray) -> np.ndarray:
    """Softmax stabil secara numerik dengan pengurangan nilai maksimum."""
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def similaritas_sesi(V: np.ndarray) -> np.ndarray:
    """Menghitung matriks kohesi kesamaan kosinus antar pesan dalam sesi percakapan."""
    N = V / np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-9, None)
    return N @ N.T


def attention_mini(
    q: np.ndarray,
    K: np.ndarray,
    V: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Scaled dot-product attention: Attention(Q, K, V) = softmax(Q K^T / sqrt(d)) V."""
    d = K.shape[1]
    skor = K @ q / np.sqrt(d)
    bobot = softmax_stabil(skor)
    konteks = bobot @ V
    return konteks, bobot


def entropi_fokus(p: np.ndarray) -> float:
    """Mengukur ketajaman fokus percakapan via entropi Shannon ternormalisasi [0.0, 1.0].
    Fokus tinggi (~1.0): Percakapan terpusat kuat pada satu isu.
    Fokus rendah (~0.0): Percakapan tersebar atau multi-topik.
    """
    p = np.clip(p, 1e-12, 1.0)
    H = float(-(p * np.log(p)).sum())
    n = len(p)
    if n <= 1:
        return 1.0
    return float(np.clip(1.0 - H / np.log(n), 0.0, 1.0))


if __name__ == "__main__":
    rng = np.random.default_rng(33)
    topik = rng.normal(0, 1, 8)
    V = np.vstack([
        topik + rng.normal(0, 0.2, 8),
        topik + rng.normal(0, 0.2, 8),
        rng.normal(0, 1, 8),
    ])
    q = topik + rng.normal(0, 0.2, 8)
    konteks, bobot = attention_mini(q, V, V)
    print("Bobot attention:", np.round(bobot, 3))
    print("Skor fokus     :", round(entropi_fokus(bobot), 3))
