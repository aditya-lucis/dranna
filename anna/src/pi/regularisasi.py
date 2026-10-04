# anna/src/pi/regularisasi.py — regularisasi L2, weight decay, dan evaluasi gap generalisasi
import numpy as np


def latih_l2(
    X_tr: np.ndarray,
    y_tr: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    lam: float = 0.01,
    epoch: int = 400,
    eta: float = 0.3,
    seed: int = 2026,
) -> tuple[np.ndarray, list[tuple[int, float, float, float]]]:
    """Pelatihan dengan regularisasi L2 (Ridge) untuk mengendalikan bobot besar dan overfitting."""
    rng = np.random.default_rng(seed)
    w = rng.normal(0, 0.01, X_tr.shape[1])
    jejak = []

    for t in range(epoch):
        z = np.clip(X_tr @ w, -30.0, 30.0)
        p = 1.0 / (1.0 + np.exp(-z))
        grad = X_tr.T @ (p - y_tr) / len(y_tr) + 2.0 * lam * w
        w -= eta * grad

        if t % 100 == 0 or t == epoch - 1:
            zv = np.clip(X_val @ w, -30.0, 30.0)
            pv = 1.0 / (1.0 + np.exp(-zv))
            err_tr = float(np.mean((p > 0.5) != y_tr))
            err_val = float(np.mean((pv > 0.5) != y_val))
            jejak.append((t, round(err_tr, 3), round(err_val, 3), round(err_tr - err_val, 3)))

    return w, jejak


if __name__ == "__main__":
    rng = np.random.default_rng(13)
    X_tr = rng.normal([3.0, 1.0], 1.5, (500, 2))
    y_tr = (X_tr @ np.array([1.2, -0.8]) + 0.3 > 0).astype(float)

    X_val = rng.normal([3.4, 1.0], 1.5, (200, 2)) + rng.normal(0, 0.8, (200, 2))
    y_val = (X_val @ np.array([1.2, -0.8]) + 0.3 > 0).astype(float)

    w, jejak = latih_l2(X_tr, y_tr, X_val, y_val, lam=0.01)
    print("Jejak pelatihan L2 (epoch, err_tr, err_val, gap):")
    for b in jejak:
        print(" ", b)
    print("Norm ||w|| dengan L2:", round(float(np.linalg.norm(w)), 3))
