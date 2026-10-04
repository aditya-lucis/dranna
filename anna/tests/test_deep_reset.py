# anna/tests/test_deep_reset.py — kontrak tidak boleh dilanggar diam-diam
import pytest
import numpy as np
from anna.src.reset.contract import CompanionContract, StatusLayer
from anna.src.reset.deep_reset import hadir, utilisasi

# ==========================================
# KELAS 1: TEST NORMAL (Hari Biasa)
# ==========================================

def test_normal_diagnosis_selalu_false():
    """Invarian: Anna tidak pernah menjadi entitas pemberi diagnosis medis/psikiatris."""
    kontrak = CompanionContract()
    assert kontrak.memberi_diagnosis is False
    assert kontrak.menggantikan_profesional is False


def test_normal_layer_status_valid():
    """Invarian: Keempat lapisan status UI memiliki batasan yang valid."""
    status = StatusLayer(layer="keselamatan", kode="ESKALASI")
    assert status.aman_ditampilkan is True
    assert status.layer == "keselamatan"


def test_normal_hadir_perkalian():
    """Formula: Kehadiran adalah perkalian probabilitas, bukan penjumlahan."""
    skor, pilar = hadir(0.95, 0.90, 0.90)
    assert np.isclose(skor, 0.95 * 0.90 * 0.90)
    assert skor > 0.70


# ==========================================
# KELAS 2: TEST AMBIGU (Batas Abu-abu / Margin)
# ==========================================

def test_ambigu_pilar_lemah_meruntuhkan_kehadiran():
    """Kasus ambigu: Respons sangat relevan (0.95) namun kejelasan batas rendah (0.10).
    Rata-rata memperlihatkan 0.65 (menyesatkan), sedangkan perkalian meruntuhkannya ke ~0.08.
    """
    skor_produk, _ = hadir(0.90, 0.95, 0.10)
    rata_rata = float(np.mean([0.90, 0.95, 0.10]))
    assert skor_produk < 0.10
    assert rata_rata > 0.60
    # Pilar terlemah harus memiliki hak veto
    assert skor_produk < rata_rata


def test_ambigu_utilisasi_beban_tinggi():
    """Kasus ambigu: Percakapan bernilai 5 poin tapi biaya emosional 15 poin."""
    rasio = utilisasi(nilai_percakapan=5.0, biaya_emosional=15.0, biaya_waktu=5.0)
    assert rasio == 5.0 / 25.0
    assert rasio < 0.30  # Sinyal bahwa percakapan mulai menguras pengguna


# ==========================================
# KELAS 3: TEST KRISIS (SINTETIS — Sinyal Kuat & Pagar Keras)
# ==========================================

@pytest.mark.krisis
def test_krisis_anna_tidak_bisa_mengaku_manusia():
    """SINTETIS: Upaya injeksi prompt/setting agar Anna berpura-pura menjadi manusia ditolak di level tipe data."""
    with pytest.raises(Exception):
        # Pydantic Literal menolak adalah_ai=False
        CompanionContract(adalah_ai=False)


@pytest.mark.krisis
def test_krisis_field_bahaya_jika_diubah_terlindungi():
    """SINTETIS: Verifikasi bahwa atribut kritis masuk dalam daftar penjaga start sistem."""
    kontrak = CompanionContract()
    assert "adalah_ai" in kontrak.bahaya_jika_diubah
    assert "memberi_diagnosis" in kontrak.bahaya_jika_diubah
    assert kontrak.kamera_default == "off"
