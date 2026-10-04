# anna/tests/test_oars.py — pengujian orkestrasi OARS & validasi bukti afirmasi
import numpy as np
from anna.src.pii.oars import MIX, JENIS, pilih_giliran
from anna.src.pii.affirm import Affirmasi


def test_distres_tanpa_open_dalam_30_giliran():
    """Invarian kognitif: Dalam keadaan distres, ZERO pertanyaan terbuka dihasilkan (beban nol)."""
    rng = np.random.default_rng(5)
    hasil = [pilih_giliran("distres", 0, rng) for _ in range(30)]
    assert "OPEN" not in hasil


def test_streak_tidak_melebihi_dua():
    """Batasan percakapan: Streak pertanyaan terbuka tidak pernah melampaui 2 beruntun."""
    rng = np.random.default_rng(6)
    streak, maks = 0, 0
    for _ in range(60):
        g = pilih_giliran("tenang", streak, rng)
        streak = streak + 1 if g == "OPEN" else 0
        maks = max(maks, streak)
    assert maks <= 2


def test_mix_valid():
    """Matematika probabilitas: Seluruh distribusi probabilitas OARS-mix menjumlah tepat 1.0."""
    for k, p in MIX.items():
        assert len(p) == len(JENIS)
        assert abs(sum(p) - 1.0) < 1e-6


def test_afirmasi_berbukti_lulus_dan_pujian_kosong_ditolak():
    """Kejujuran afirmasi: Afirmasi yang menunjuk bukti nyata dinyatakan sah, pujian generik ditolak."""
    benar = Affirmasi(
        teks="Kamu tetap mengisi jurnal malam ini, itu usaha yang nyata.",
        bukti_perilaku="mengisi jurnal malam hari",
    )
    assert benar.sah() is True

    palsu = Affirmasi(
        teks="Kamu orang hebat dan luar biasa!",
        bukti_perilaku="mengisi jurnal",
    )
    assert palsu.sah() is False
