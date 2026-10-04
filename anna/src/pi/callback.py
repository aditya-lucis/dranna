# anna/src/pi/callback.py — pencatat jejak loss pembelajaran (observabilitas LangSmith-style)
import numpy as np


def latih_dengan_jejak(
    X: np.ndarray,
    y: np.ndarray,
    epoch: int = 200,
    eta: float = 0.1,
    catat_tiap: int = 40,
    seed: int = 2026,
) -> tuple[np.ndarray, list[tuple[int, float]]]:
    """Melatih model sambil merekam jejak loss per epoch untuk transparansi audit."""
    rng = np.random.default_rng(seed)
    w = rng.normal(0, 0.01, X.shape[1])
    jejak = []

    for t in range(epoch):
        p = 1.0 / (1.0 + np.exp(-np.clip(X @ w, -30.0, 30.0)))
        eps = 1e-9
        loss = -float(np.mean(y * np.log(p + eps) + (1.0 - y) * np.log(1.0 - p + eps)))

        if t % catat_tiap == 0 or t == epoch - 1:
            jejak.append((t, round(loss, 4)))

        grad = X.T @ (p - y) / len(y)
        w -= eta * np.clip(grad, -5.0, 5.0)

    return w, jejak


if __name__ == "__main__":
    rng = np.random.default_rng(9)
    n = 400
    X = np.vstack([
        rng.normal([2.0, 0.5], 1.2, (n // 2, 2)),
        rng.normal([6.0, 3.0], 1.4, (n // 2, 2)),
    ])
    y = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
    w, jejak = latih_dengan_jejak(X, y)
    print("Jejak loss pelatihan (harus turun melandai):", jejak)
