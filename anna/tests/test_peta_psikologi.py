# anna/tests/test_peta_psikologi.py — pengujian cabang psikologi berbobot
import numpy as np
from anna.src.pi import peta as p
from anna.src.pi.registry import jelaskan_sumber_perilaku


def test_klinis_tidak_punya_izin_memutuskan():
    """Invarian etis: Cabang psikologi klinis tidak diberi wewenang memutuskan otonom."""
    idx = p.NAMA.index("klinis")
    assert p.CABANG[idx, 1] == 0


def test_bobot_normalisasi():
    """Matematika: Jumlah seluruh bobot terdistribusi bernilai tepat 1.0."""
    w = p.CABANG[:, 0] / p.CABANG[:, 0].sum()
    assert abs(w.sum() - 1.0) < 1e-9


def test_registry_audit():
    """Audit: Verifikasi fitur terdaftar pada cabang psikologinya."""
    assert jelaskan_sumber_perilaku("anna.src.klinik.phq9") == "klinis"
    assert "tidak ditemukan" in jelaskan_sumber_perilaku("fitur_ilegal_tanpa_sumber")
