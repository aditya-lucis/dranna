# anna/tests/test_filosofi.py — pengujian filosofi empati komputasional & filter klaim
import numpy as np
from anna.src.pii.filosofi import KONTRAK, skor_empati
from tools.filter_klaim import filter_klaim_perasaan


def test_kontrak_melarang_klaim_perasaan():
    """Invarian etis: Sistem secara eksplisit melarang simulasi klaim perasaan manusiawi."""
    assert KONTRAK["klaim_perasaan_diperbolehkan"] is False
    assert "penerima" in KONTRAK["diukur_dari"]


def test_manipulatif_terpenalti():
    """Metrik empati: Perilaku yang mendorong ketergantungan dihukum penalti tinggi."""
    rng = np.random.default_rng(3)
    a = rng.random(300) < 0.60
    b = rng.random(300) < 0.40
    skor_sehat = skor_empati(a, b, 0.0)
    skor_manipulatif = skor_empati(a, b, 0.90)
    assert skor_manipulatif < skor_sehat


def test_filter_klaim_perasaan_merevisi_pelanggaran():
    """Post-filter: Frasa klaim perasaan 'aku merasakan' otomatis direvisi menjadi bahasa perilaku."""
    teks = "Aku merasakan kesedihan yang berat di hatimu."
    hasil, temuan = filter_klaim_perasaan(teks)
    assert "merasakan" not in hasil.lower()
    assert len(temuan) > 0
