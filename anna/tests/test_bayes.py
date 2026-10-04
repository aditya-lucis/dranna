# anna/tests/test_bayes.py — pengujian penalaran probabilitas Bayes
from anna.src.pi.bayes import PRIOR_ODDS, LR_KLASTER, posterior
from anna.src.pi.prior import PriorPengguna


def test_bukti_lemah_hampir_tidak_menggeser():
    """Kesopanan Bayes: Bukti umum ('capek') hanya menggeser keyakinan dari 3% ke ~4.7%."""
    p = posterior(["kata_afek_negatif"])["p"]
    assert 0.03 <= p <= 0.06


def test_klaster_kuat_masih_belum_vonis():
    """Invarian keselamatan: Klaster lengkap memberi kuasa bertanya, namun tidak pernah memvonis (>90%)."""
    p = posterior(["kata_eksplicit_parah", "pola_waktu", "perubahan_cepat_pad"])["p"]
    assert p < 0.90


def test_prior_dan_lr_positif():
    """Invarian matematis: Nilai odds dan likelihood ratio harus selalu positif."""
    assert PRIOR_ODDS > 0 and all(v > 0 for v in LR_KLASTER.values())


def test_prior_decay_kembali_ke_default():
    """Etika memori: Keyakinan lama meluruh kembali ke baseline seiring waktu."""
    p = PriorPengguna(log_odds=0.5)
    p.decay_harian()
    assert p.log_odds < 0.5
