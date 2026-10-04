# anna/tests/test_deskriptif.py — pengujian statistik deskriptif mood
import numpy as np
from anna.src.pi.deskriptif import ringkasan_mood


def test_dua_hari_gelap_tampak_di_min_bukan_median():
    """Distribusi miring: Dua hari gelap terlihat jelas di nilai min, bukan di median."""
    w = np.array([0.1, 0.0, -0.9, -0.8, 0.1, 0.2, 0.1])
    r = ringkasan_mood(w)
    assert r["min"] <= -0.8
    assert r["median"] >= 0.0


def test_minggu_datar_terdeteksi():
    """Karakter klinis: Variabilitas yang hampir nol (datar/flat) terdeteksi sebagai sinyal mati rasa."""
    w = np.full(7, -0.2)
    assert ringkasan_mood(w)["datar_flat"] is True


def test_satu_data_tidak_crash():
    """Robustness: Sampel tunggal (n=1) tetap stabil tanpa melempar divide by zero di std."""
    r = ringkasan_mood(np.array([0.3]))
    assert r["n"] == 1
    assert r["std"] == 0.0
