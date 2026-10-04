# anna/tests/test_pca.py — pengujian PCA SVD & deteksi anomali residu
import numpy as np
from anna.src.pi.pca import pca, residu_pca
from anna.src.pi.anomali import deteksi_hari_tak_biasa


def test_varian_ratio_urut_dan_jumlah_satu():
    """Matematika SVD: Rasio variansi terurut menurun dan menjumlah tepat 1.0."""
    rng = np.random.default_rng(1)
    X = rng.normal(0, 1, (50, 5))
    _, _, ratio = pca(X, k=5)
    assert np.all(np.diff(ratio) <= 1e-9)
    assert abs(ratio.sum() - 1.0) < 1e-9


def test_pca_menemukan_arah_dominan():
    """Proyeksi: PCA menangkap arah variasi terbesar pada data 1-dimensi tersembunyi."""
    rng = np.random.default_rng(2)
    arah = np.array([0.9, 0.1, 0.4])
    arah = arah / np.linalg.norm(arah)
    t = rng.normal(0, 3, 200)
    X = np.outer(t, arah) + rng.normal(0, 0.1, (200, 3))

    _, V_k, ratio = pca(X, k=1)
    assert ratio[0] > 0.95
    assert abs(abs(float(V_k[0, 0])) - abs(arah[0])) < 0.05


def test_residu_anomali_lebih_besar():
    """Deteksi anomali: Titik pencilan yang melanggar korelasi memiliki residu rekonstruksi terbesar."""
    rng = np.random.default_rng(3)
    t = rng.normal(0, 2, (40, 1))
    X = np.hstack([t, t, t]) + rng.normal(0, 0.2, (40, 3))
    X[7] = np.array([8.0, -8.0, 8.0])  # Injeksi pencilan yang melanggar korelasi
    res = residu_pca(X, k=1)
    assert np.argmax(res) == 7

    anomali = deteksi_hari_tak_biasa(X, k=1)
    assert 7 in anomali
