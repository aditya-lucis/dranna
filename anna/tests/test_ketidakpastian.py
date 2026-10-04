# anna/tests/test_ketidakpastian.py — pengujian interval kepercayaan & kalibrasi ECE
import numpy as np
from anna.src.pi.bootstrap import bootstrap_median, ci_t
from anna.src.pi.kalibrasi import ece


def test_ci_mengandung_mean_sampel():
    """Validasi statistika: Interval kepercayaan Student-t harus merangkum rata-rata sampel."""
    rng = np.random.default_rng(3)
    x = rng.normal(-0.2, 0.4, 21)
    lo, hi = ci_t(x)
    assert lo < x.mean() < hi


def test_bootstrap_konsisten_sampel_besar():
    """Nonparametrik: Bootstrap median sampel besar mencakup nilai ekspektasi populasi."""
    rng = np.random.default_rng(4)
    x = rng.normal(0.1, 0.3, 500)
    lo, hi = bootstrap_median(x, B=800)
    assert lo <= 0.1 <= hi


def test_sampel_kecil_tidak_crash():
    """Robustness: Sampel tunggal (n=1) tidak melempar ZeroDivisionError dan bernilai finite."""
    lo, hi = ci_t(np.array([0.5]))
    assert np.isfinite(lo + hi)


def test_ece_terkalibrasi_rendah():
    """Kalibrasi: Prediksi yang selaras dengan peluang kebenaran memiliki skor ECE rendah (<0.05)."""
    rng = np.random.default_rng(11)
    yakin = rng.uniform(0.1, 0.9, 1000)
    benar = rng.random(1000) < yakin
    assert ece(yakin, benar) < 0.05
