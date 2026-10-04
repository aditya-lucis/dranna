# anna/src/pi/naive_bayes.py — deteksi suasana dari nol via Naive Bayes (log-space + Laplace)
import numpy as np

KELAS = ["berat", "biasa", "terang"]

# Data latih sintetis awal (SINTETIS — bukan transkrip pengguna nyata)
LATIH = {
    "berat": [
        "aku nggak sanggup lagi", "semuanya terasa hampa",
        "capek hidup kayaknya", "nggak ada gunanya semua ini",
        "aku gagal terus"
    ],
    "biasa": [
        "hari biasa aja", "kerja seperti biasa",
        "agak capek tapi oke", "meeting panjang tadi",
        "makan siang enak"
    ],
    "terang": [
        "aku senang banget hari ini", "kabar baik datang",
        "leganya akhirnya selesai", "senyum terus tadi",
        "besok libur rasanya"
    ],
}


def latih(alpha: float = 1.0) -> tuple[dict, dict, list[str]]:
    """Melatih Naive Bayes dengan smoothing Laplace."""
    vocab = set()
    model = {}
    for c, docs in LATIH.items():
        kata = " ".join(docs).split()
        vocab.update(kata)
        model[c] = {k: kata.count(k) for k in set(kata)}

    V = len(vocab)
    prior = {}
    total_docs = sum(len(d) for d in LATIH.values())
    for c, docs in LATIH.items():
        total_tokens = sum(model[c].values()) + alpha * V
        prior[c] = float(np.log(len(docs) / total_docs))
        model[c] = {k: (n + alpha) / total_tokens for k, n in model[c].items()}

    return model, prior, sorted(vocab)


MODEL, PRIOR, VOCAB = latih()


def prediksi(pesan: str, model=None, prior=None, vocab=None) -> dict:
    """Prediksi suasana di log-space dengan kalkulasi margin kerendahan hati."""
    m = model or MODEL
    pr = prior or PRIOR
    v = vocab or VOCAB

    skor = {}
    bukti = {}
    kata_list = pesan.lower().split()

    for c in KELAS:
        s = pr[c]
        default_prob = 1.0 / (len(m[c]) + len(v) + 1.0)
        for w in kata_list:
            p_wc = m[c].get(w, default_prob)
            log_p = float(np.log(p_wc))
            s += log_p
            bukti.setdefault(c, []).append((w, round(log_p, 3)))
        skor[c] = s

    c_hat = max(skor, key=skor.get)
    sorted_skors = sorted(skor.values())
    margin = sorted_skors[-1] - sorted_skors[-2] if len(sorted_skors) >= 2 else 0.0

    return {
        "kelas": c_hat,
        "log_skor": {k: round(float(val), 2) for k, val in skor.items()},
        "margin": round(float(margin), 2),
        "kata_penting": sorted(bukti.get(c_hat, []), key=lambda t: t[1])[:3],
    }


if __name__ == "__main__":
    print(prediksi("aku capek dan nggak sanggup"))
    print(prediksi("leganya selesai kabar baik"))
