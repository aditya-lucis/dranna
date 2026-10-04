# anna/tests/test_attention.py — pengujian mekanisme attention mini & stabilitas softmax
import numpy as np
from anna.src.pi.attention import (
    attention_mini,
    entropi_fokus,
    softmax_stabil,
)


def test_softmax_jumlah_satu_dan_stabil():
    """Stabilitas numerik: Softmax stabil pada input nilai eksponensial besar (1000.0) dan menjumlah tepat 1."""
    z = np.array([1000.0, 1000.0, 999.0])
    p = softmax_stabil(z)
    assert np.allclose(p.sum(), 1.0)
    assert np.all(np.isfinite(p))


def test_attention_mengabaikan_melenceng():
    """Selektivitas: Pesan yang melenceng topik menerima bobot kecil (<0.1), pesan relevan mendominasi (>0.85)."""
    rng = np.random.default_rng(1)
    topik = rng.normal(0, 1, 8)
    V = np.vstack([topik + rng.normal(0, 0.1, 8) for _ in range(3)] + [rng.normal(0, 1, 8)])
    q = topik + rng.normal(0, 0.1, 8)
    _, bobot = attention_mini(q, V, V)
    assert bobot[-1] < 0.1
    assert bobot[:3].sum() > 0.85


def test_fokus_identitas_dan_rata():
    """Entropi: Distribusi satu titik (one-hot) bernilai fokus ~1.0, sedangkan distribusi rata bernilai ~0.0."""
    n = 5
    fokus_seragam = entropi_fokus(np.ones(n) / n)
    e = np.zeros(n)
    e[0] = 1.0
    fokus_tajam = entropi_fokus(e)
    assert fokus_tajam > 0.99
    assert fokus_seragam < 0.01
