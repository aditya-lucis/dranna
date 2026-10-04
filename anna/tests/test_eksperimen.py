# anna/tests/test_eksperimen.py — pengujian praregistrasi & validasi statistik
import numpy as np
from anna.src.pi.eksperimen import PRAREGISTRASI, cohen_d_ci, daya_diperlukan
from anna.src.pi.eval_config import EvaluasiKontrol


def test_praregistrasi_terkunci():
    """Invarian: Metrik utama dikunci sebelum data dilihat dan n minimum dipenuhi."""
    assert PRAREGISTRASI["metric_utama"] == "skor_beban_mingguan"
    assert PRAREGISTRASI["n_rencana_per_grup"] >= 30


def test_null_memberi_hasil_gagal():
    """Kejujuran sains: Dua sampel dari distribusi identik menghasilkan verdict yang tidak overclaim."""
    rng = np.random.default_rng(1)
    a = rng.normal(0, 1, 200)
    b = rng.normal(0, 1, 200)
    hasil = cohen_d_ci(a, b)
    assert hasil["berhasil_prareg"] is False or abs(hasil["d"]) < 0.2


def test_daya_naik_saat_efek_kecil():
    """Power analysis: Mendeteksi efek kecil (d=0.25) menuntut ukuran sampel yang jauh lebih besar daripada d=0.5."""
    assert daya_diperlukan(0.5) < daya_diperlukan(0.25)


def test_evaluasi_kontrol_label_jujur():
    """Etika klaim: Bila CI bawah <= 0, fitur diberi label 'belum terbukti — jangan diiklankan'."""
    kontrol = EvaluasiKontrol()
    label = kontrol.label_hasil(d=0.15, ci_lo=-0.02)
    assert "belum terbukti" in label
