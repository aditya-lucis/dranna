# anna/src/pi/pca.py — reduksi dimensi longitudinal SVD / PCA & kalkulasi residu
import numpy as np


def pca(
    X: np.ndarray,
    k: int = 2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Dekomposisi SVD untuk proyeksi data mood longitudinal ke k sumbu utama.
    Mengembalikan (Z_proyeksi, V_k, variance_ratio).
    """
    Xc = X - X.mean(axis=0)
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    total_var = (s ** 2).sum()
    ratio = (s ** 2) / total_var if total_var > 0 else np.zeros_like(s)
    return Xc @ Vt[:k].T, Vt[:k].T, ratio


def residu_pca(X: np.ndarray, k: int = 2) -> np.ndarray:
    """Menghitung jarak Euclidean (residu rekonstruksi) tiap titik ke sub-ruang k-dimensi."""
    Xc = X - X.mean(axis=0)
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    V_k = Vt[:k].T
    proyeksi = Xc @ V_k @ V_k.T
    return np.linalg.norm(Xc - proyeksi, axis=1)


if __name__ == "__main__":
    rng = np.random.default_rng(2026)
    n = 28
    X = rng.normal(0, 1, (n, 6))
    Zs = (X - X.mean(0)) / X.std(0)
    Z, V_k, ratio = pca(Zs, k=2)
    print("Variance ratio 2 komponen teratas:", np.round(ratio[:2], 3))
