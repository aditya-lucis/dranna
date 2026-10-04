# anna/tests/test_regularisasi.py — pengujian regularisasi L2 dan pencegahan hafalan
import numpy as np
from anna.src.pi.regularisasi import latih_l2
from anna.src.pi.eval_gate import gerbang_rilis


def test_l2_mengecilkan_norma_bobot():
    """Matematika L2: Koefisien penalti lambda > 0 terbukti menarik turun magnitude norma vektor bobot ||w||."""
    rng = np.random.default_rng(6)
    X = rng.normal(0.0, 2.0, (300, 3))
    y = (X @ [1.0, -1.0, 0.0] > 0).astype(float)
    Xv, yv = X[:80].copy(), y[:80].copy()

    w_tanpa_l2, _ = latih_l2(X, y, Xv, yv, lam=0.0, epoch=150)
    w_dengan_l2, _ = latih_l2(X, y, Xv, yv, lam=0.05, epoch=150)

    assert np.linalg.norm(w_dengan_l2) < np.linalg.norm(w_tanpa_l2)


def test_gap_terdeteksi_di_domain_shift():
    """Generalisasi: Pergeseran domain pada data validasi terdeteksi lewat melebarnya selisih error."""
    rng = np.random.default_rng(7)
    X = rng.normal(0.0, 1.5, (400, 2))
    y = (X @ [1.0, -0.5] > 0).astype(float)
    Xs = X[:100] + rng.normal(0.0, 1.0, (100, 2))  # Injeksi noise domain shift

    w, jejak = latih_l2(X, y, Xs, y[:100], epoch=120)
    err_tr, err_val, gap = jejak[-1][1:]
    assert gap <= 0.0  # Error validasi lebih besar dari error latih


def test_gerbang_rilis_menahan_model_overfit():
    """Kebijakan rilis: Model baru dengan gap berlebih otomatis ditahan dari promosi."""
    baseline = {"err_val": 0.10, "gap": 0.05}
    keputusan = gerbang_rilis(err_val_baru=0.15, gap_baru=0.25, baseline=baseline)
    assert keputusan["lolos"] is False
    assert keputusan["keputusan"] == "kandidat ditahan"
