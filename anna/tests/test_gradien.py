# anna/tests/test_gradien.py — pengujian kalkulus gradient descent & sigmoid stabil
import numpy as np
from anna.src.pi.gradien import bce_grad, latih_logreg, sigmoid


def test_sigmoid_stabil_ekstrem():
    """Stabilitas numerik: Sigmoid tidak menghasilkan NaN atau inf pada input ekstrem ±800."""
    z = np.array([-800.0, 0.0, 800.0])
    p = sigmoid(z)
    assert np.all(np.isfinite(p))
    assert np.allclose(p[1], 0.5)
    assert p[0] == 0.0
    assert p[2] == 1.0


def test_grad_nol_di_prediksi_sempurna():
    """Kalkulus: Gradien bernilai nol jika probabilitas prediksi tepat sama dengan label."""
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    w = np.array([0.0, 0.0])
    y = np.array([0.5, 0.5])  # Saat w=0, sigmoid(X @ w) = 0.5
    assert np.allclose(bce_grad(X, y, w), 0.0, atol=1e-9)


def test_latih_memisahkan_kelas():
    """Optimisasi: Model mampu belajar memisahkan dua klaster data linear yang terpisah tegas."""
    rng = np.random.default_rng(2)
    X = np.vstack([rng.normal(-3.0, 0.8, (60, 2)), rng.normal(3.0, 0.8, (60, 2))])
    y = np.concatenate([np.zeros(60), np.ones(60)])
    w = latih_logreg(X, y, epoch=300, eta=0.2)
    assert sigmoid(np.array([3.0, 3.0]) @ w) > 0.85
    assert sigmoid(np.array([-3.0, -3.0]) @ w) < 0.15
