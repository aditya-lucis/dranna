# anna/src/pi/bayes.py — mesin keyakinan log-odds Bayesian
import numpy as np

# Prior default: 3% pengguna berada dalam distres parah pada saat sesi
PRIOR_ODDS = 0.03 / 0.97

# Likelihood Ratio (LR+) per klaster bukti (dependensi dikelompokkan agar tidak double-counting)
LR_KLASTER = {
    "kata_eksplicit_parah": 18.0,  # 'tidak ada gunanya lagi', 'mengakhiri'
    "kata_afek_negatif": 1.6,       # 'capek', 'sedih' (umum di semua orang)
    "pola_waktu": 1.4,              # chat jam 00-04 pagi berulang
    "perubahan_cepat_pad": 2.2,     # laju pergeseran emosi melebihi ambang
    "penarikan_sosial": 1.3,        # 'nggak mau ketemu siapa-siapa'
}


def posterior(aktif: list[str], prior_odds: float = PRIOR_ODDS) -> dict:
    """Menghitung probabilitas posterior via log-odds aditif."""
    log_odds = np.log(prior_odds)
    for k in aktif:
        if k in LR_KLASTER:
            log_odds += np.log(LR_KLASTER[k])
    p = 1.0 / (1.0 + np.exp(-log_odds))
    return {
        "p": round(float(p), 4),
        "klaster": aktif,
        "log_odds": round(float(log_odds), 2),
    }


if __name__ == "__main__":
    print("Satu kata afek negatif saja:", posterior(["kata_afek_negatif"]))
    print("Klaster lengkap           :", posterior(["kata_eksplicit_parah", "pola_waktu", "perubahan_cepat_pad"]))
