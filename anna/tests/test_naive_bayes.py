# anna/tests/test_naive_bayes.py — pengujian detektor suasana Naive Bayes
import numpy as np
from anna.src.pi.naive_bayes import latih, prediksi


def test_latih_dan_prediksi_konsisten():
    """Konsistensi: Detektor mampu mengklasifikasi pesan polar terang vs berat secara benar."""
    model, prior, vocab = latih()
    assert prediksi("aku senang banget", model, prior, vocab)["kelas"] == "terang"
    assert prediksi("semuanya hampa", model, prior, vocab)["kelas"] == "berat"


def test_kata_asing_tidak_membunuh():
    """Laplace smoothing: Keberadaan kata acak/asing tidak mematikan probabilitas kata lainnya."""
    model, prior, vocab = latih()
    r = prediksi("aku senang zyqx banget", model, prior, vocab)
    assert r["kelas"] == "terang"


def test_log_space_stabil():
    """Stabilitas numerik: 500 kata tak dikenal tetap menghasilkan skor finite tanpa overflow/underflow."""
    model, prior, vocab = latih()
    pesan = " ".join(["zzz"] * 500)
    r = prediksi(pesan, model, prior, vocab)
    assert all(np.isfinite(v) for v in r["log_skor"].values())
