# anna/tests/test_numerik.py — pengujian stabilitas floating point & penolak NaN/Inf
import numpy as np
import pytest
from anna.src.pi.numerik import logsumexp, softmax_lse, zscore_klinik
from anna.src.pi.guard import skor_mood


def test_logsumexp_tanpa_inf():
    """Numerik: logsumexp aman dari overflow pada nilai 1000.0."""
    z = np.array([1000.0, 1000.0, 999.0])
    assert np.isfinite(logsumexp(z))


def test_softmax_jumlah_satu_di_ekstrem():
    """Numerik: softmax_lse aman pada input ekstrem dan menjumlah tepat 1.0."""
    z = np.array([800.0, 799.0, -800.0])
    p = softmax_lse(z)
    assert np.allclose(p.sum(), 1.0)
    assert np.all(np.isfinite(p))


def test_zscore_kolom_konstan():
    """Numerik: Standardisasi z-score tidak membagi dengan nol ketika deviasi standar kolom bernilai nol."""
    X = np.array([[1.0, 5.0], [1.0, 7.0]])
    Z = zscore_klinik(X)
    assert np.all(np.isfinite(Z))
    assert np.all(Z[:, 0] == 0.0)


def test_guard_menolak_nan():
    """Invarian keselamatan: Fungsi yang menilai manusia wajib melempar ValueError saat menerima input NaN."""
    with pytest.raises(ValueError):
        skor_mood(np.array([[1.0, np.nan, 2.0]]))
