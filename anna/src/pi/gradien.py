# anna/src/pi/gradien.py — gradient descent BCE berbobot dari nol (NumPy murni)
import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Fungsi sigmoid stabil secara numerik (menghindari exp overflow)."""
    z = np.asarray(z, dtype=np.float64)
    out = np.empty_like(z, dtype=np.float64)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def bce_grad(X: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Turunan gradien Binary Cross-Entropy: grad = (1/n) * X^T (p - y)."""
    p = sigmoid(X @ w)
    return X.T @ (p - y) / len(y)


def latih_logreg(
    X: np.ndarray,
    y: np.ndarray,
    epoch: int = 300,
    eta: float = 0.1,
    alpha_kelas: float = 0.7,
    seed: int = 2026,
) -> np.ndarray:
    """Melatih regresi logistik dari nol dengan bobot asimetris alpha (kebijakan etis).
    alpha_kelas = 0.7: Lebih menghukum False Negative distres.
    """
    rng = np.random.default_rng(seed)
    w = rng.normal(0, 0.01, X.shape[1])
    bobot = np.where(y == 1, alpha_kelas, 1.0 - alpha_kelas)

    for _ in range(epoch):
        p = sigmoid(X @ w)
        grad = X.T @ (bobot * (p - y)) / bobot.sum()
        w -= eta * np.clip(grad, -5.0, 5.0)  # Clipping anti-meledak

    return w


if __name__ == "__main__":
    rng = np.random.default_rng(9)
    n = 400
    X_sehat = rng.normal([2.0, 0.5], 1.2, (n // 2, 2))
    X_distres = rng.normal([6.0, 3.0], 1.4, (n // 2, 2))
    X = np.vstack([X_sehat, X_distres])
    y = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
    w = latih_logreg(X, y)
    print("Bobot model:", np.round(w, 3))
    uji = np.array([[7.5, 3.4], [1.5, 0.3]])
    print("P(distres) uji:", np.round(sigmoid(uji @ w), 3))
