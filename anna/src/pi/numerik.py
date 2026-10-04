# anna/src/pi/numerik.py — disiplin numerik floating point, log-sum-exp & shape guard
import numpy as np


def logsumexp(z: np.ndarray, axis: int = -1) -> np.ndarray:
    """Perhitungan log-sum-exp stabil untuk menghindari overflow eksponensial."""
    z = np.asarray(z, dtype=np.float64)
    m = np.max(z, axis=axis, keepdims=True)
    res = m + np.log(np.exp(z - m).sum(axis=axis, keepdims=True))
    if axis is None:
        return float(res)
    return res.squeeze(axis)


def softmax_lse(z: np.ndarray) -> np.ndarray:
    """Softmax terkalibrasi via normalisasi titik puncak maksimum."""
    z = np.asarray(z, dtype=np.float64)
    z_geser = z - z.max(axis=-1, keepdims=True)
    return np.exp(z_geser) / np.exp(z_geser).sum(axis=-1, keepdims=True)


def zscore_klinik(X: np.ndarray) -> np.ndarray:
    """Standardisasi z-score dengan shape-guard ketat 2D dan penanganan kolom konstan (sd=0)."""
    assert X.ndim == 2, f"data klinis harus 2D, dapat dimensi {X.shape}"
    mu = X.mean(axis=0, keepdims=True)
    sd = X.std(axis=0, keepdims=True)
    return (X - mu) / np.where(sd == 0.0, 1.0, sd)


if __name__ == "__main__":
    print("logsumexp([1000, 999]):", logsumexp(np.array([1000.0, 999.0])))
    print("softmax_lse([800, 799]):", softmax_lse(np.array([800.0, 799.0])))
