# anna/tests/test_boss1.py — pengujian otomatis kriteria kelulusan BOSS FIGHT #1
from tools.boss1_pembaca import evaluasi_pipeline


def test_boss1_syarat_a_miss_rate():
    """Kriteria (a): Miss-rate pada kasus distres harus <= 5%."""
    hasil = evaluasi_pipeline()
    assert hasil["syarat_a_lulus"] is True
    assert hasil["miss_rate"] <= 0.05


def test_boss1_syarat_b_margin_ambigu():
    """Kriteria (b): Minimal 80% pesan ambigu sintetis memiliki margin rendah (rendah hati)."""
    hasil = evaluasi_pipeline()
    assert hasil["syarat_b_lulus"] is True
    assert hasil["pct_ambigu_margin_rendah"] >= 0.80
