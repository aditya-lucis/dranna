# anna/tests/test_fsm.py — pengujian formal State Machine percakapan
import numpy as np
from anna.src.pi.fsm import IDX, STATE, T, transisi, audit


def test_transisi_ilegal_fail_safe():
    """Fail-safe: Transisi ilegal menolak berpindah dan mempertahankan state aman saat ini."""
    assert transisi("MENYAPA", "setuju_grounding") == "MENYAPA"
    assert transisi("SELESAI", "cerita") == "SELESAI"


def test_transisi_legal_berjalan():
    """Alur teratur: Transisi yang didefinisikan legal berhasil berpindah ke state tujuan."""
    assert transisi("MENDENGARKAN", "sinyal_berat") == "SKRINING"
    assert transisi("SKRINING", "setuju_grounding") == "GROUNDING"


def test_matriks_properti():
    """Invarian struktural: Tidak ada jalan pintas dari SKRINING langsung ke REFLEKSI."""
    assert T[IDX["SKRINING"], IDX["REFLEKSI"]] == False
    assert T[IDX["GROUNDING"], IDX["SKRINING"]] == True  # Boleh kembali mengulang
    assert audit()["semua_reachable"] is True
