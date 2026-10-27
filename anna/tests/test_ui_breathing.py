# anna/tests/test_ui_breathing.py — pengujian siklus pernapasan 4-7-8
from anna.src.pix.breathing_widget import PengaturNapas478


def test_fase_tarik():
    s = PengaturNapas478.hitung_status(2.0)
    assert s.fase == "tarik"
    assert s.siklus_ke == 1
    assert "hidung" in s.instruksi


def test_fase_tahan():
    s = PengaturNapas478.hitung_status(6.0)  # Detik 6: 4s tarik + 2s tahan
    assert s.fase == "tahan"
    assert s.detik_dalam_fase == 2.0


def test_fase_hembus():
    s = PengaturNapas478.hitung_status(14.0)  # Detik 14: 4s tarik + 7s tahan + 3s hembus
    assert s.fase == "hembuskan"
    assert s.detik_dalam_fase == 3.0


def test_siklus_berikutnya():
    s = PengaturNapas478.hitung_status(20.0)  # Siklus ke-2 detik ke-1
    assert s.siklus_ke == 2
    assert s.fase == "tarik"
