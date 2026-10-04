# anna/src/pi/bootstrap.py — interval kepercayaan & bootstrap nonparametrik
import numpy as np
from scipy import stats


def ci_t(x: np.ndarray, alpha: float = 0.05) -> tuple[float, float]:
    """CI mean via distribusi Student-t untuk sampel kecil."""
    x = np.asarray(x, dtype=float)
    n = x.size
    if n <= 1:
        val = float(x[0]) if n == 1 else 0.0
        return (val, val)

    t_kritis = stats.t.ppf(1 - alpha / 2, df=n - 1)
    half = t_kritis * x.std(ddof=1) / np.sqrt(n)
    return (round(float(x.mean() - half), 3), round(float(x.mean() + half), 3))


def bootstrap_median(x: np.ndarray, B: int = 2000, seed: int = 2026) -> tuple[float, float]:
    """CI median via bootstrap nonparametrik tanpa asumsi bentuk distribusi."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    n = x.size
    if n == 0:
        return (0.0, 0.0)

    idx = rng.integers(0, n, size=(B, n))
    meds = np.median(x[idx], axis=1)
    lo, hi = np.percentile(meds, [2.5, 97.5])
    return (round(float(lo), 3), round(float(hi), 3))


if __name__ == "__main__":
    minggu = np.array([0.1, 0.0, -0.9, -0.8, 0.1, 0.2, 0.1])
    print("mean      :", round(minggu.mean(), 3))
    print("CI-t mean :", ci_t(minggu))
    print("CI median :", bootstrap_median(minggu))
