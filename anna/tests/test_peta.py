# anna/tests/test_peta.py — arsitektur punya invarian yang bisa diuji
from anna.src.reset.peta import LAPIS, PetaSerenity


def test_safety_adalah_veto_tertinggi():
    """Invarian: Hanya lapisan safety yang memiliki hak veto atas semua lapisan lain."""
    peta = PetaSerenity()
    assert peta.veto_tertinggi == "safety"


def test_sepuluh_lapisan_lengkap():
    """Invarian: Tepat sepuluh lapisan arsitektural terdefinisi dalam urutan kanonik."""
    assert len(LAPIS) == 10
    assert LAPIS[3][0] == "safety"  # Lapis ke-4 (index 3) adalah safety gate


def test_init_data_dulu_ui_terakhir():
    """Invarian: Komponen penyimpanan/persepsi dibangun terlebih dahulu, UI selalu paling akhir."""
    urutan = PetaSerenity().urutan_init()
    assert urutan[-1] == "ui"
    assert "memory" in urutan[:3] or "voicevis" in urutan[:3]
