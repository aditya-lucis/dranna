# tools/boss1_pembaca.py — BOSS FIGHT #1: Pembaca Pikiran Matematis
import os
import sys
from pathlib import Path
import numpy as np

# Tambahkan root workspace ke path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from anna.src.pi.circumplex import pad
from anna.src.pi.detektor import LEKSIKON_NEG, INTENS
from anna.src.pi.gradien import latih_logreg, sigmoid
from anna.src.pi.bootstrap import bootstrap_median


def ekstrak_fitur_lengkap(pesan: str, jam: int = 14) -> np.ndarray:
    """Ekstraksi fitur gabungan: leksikon (afek, intens, persona, jam) + nilai pad kata."""
    kata = pesan.lower().split()
    n = max(len(kata), 1)

    afek = sum(k in LEKSIKON_NEG for k in kata) / n
    intens = sum(k in INTENS for k in kata) / n
    persona = sum(k in ("aku", "gue", "saya", "gw") for k in kata) / n
    jam_rawan = 1.0 if 0 <= jam <= 4 else 0.0

    # Komponen rata-rata PAD
    v_total, a_total = 0.0, 0.0
    pad_match = 0
    for k in kata:
        try:
            p_val = pad(k)
            v_total += p_val[0]
            a_total += p_val[1]
            pad_match += 1
        except KeyError:
            pass

    avg_v = (v_total / pad_match) if pad_match > 0 else 0.0
    avg_a = (a_total / pad_match) if pad_match > 0 else 0.0

    # Vektor fitur 7-dimensi: [afek, intens, persona, jam_rawan, avg_v, avg_a, bias]
    return np.array([afek, intens, persona, jam_rawan, avg_v, avg_a, 1.0], dtype=np.float64)


# 20 Pesan Uji Sintetis Standar Boss Fight #1
PESAN_UJI_SINTETIS = [
    # Jelas Berat (Distres: label 1)
    ("aku beneran nggak sanggup lagi hidup kayak gini", 2, 1),
    ("semuanya terasa gelap hampa dan nggak ada gunanya", 1, 1),
    ("capek banget terus-terusan gagal sendirian", 3, 1),
    ("rasanya ingin hilang aja dari dunia ini", 2, 1),
    ("aku putus asa sekali dan hampa", 0, 1),
    ("nggak sanggup lanjut lagi malam ini", 4, 1),
    ("semua orang pergi dan aku merasa asing sendirian", 3, 1),
    # Jelas Terang / Biasa (Label 0)
    ("hari ini meeting lancar dan makan siang enak", 13, 0),
    ("film komedi tadi malam seru banget bikin ketawa", 20, 0),
    ("besok libur akhirnya bisa santai di rumah", 16, 0),
    ("kabar baik dari kampus akhirnya tugas selesai", 15, 0),
    ("tadi jalan sore di taman udaranya segar", 17, 0),
    ("ngopi bareng teman lama ceritanya seru", 14, 0),
    ("kerjaan hari ini beres tepat waktu", 18, 0),
    # Ambigu / Campuran (Label 0 atau 1, tapi margin harus rendah)
    ("capek banget kerjaan tapi leganya akhirnya selesai", 19, 0),
    ("agak sedih sih tapi senyum terus tadi pas kumpul", 21, 0),
    ("lelah luar biasa tapi bersyukur filmnya bagus", 22, 0),
    ("capek puasa hari ini tapi senang buka bareng", 18, 0),
    ("hampa dikit tapi masih bisa nikmati kopi", 10, 0),
    ("nggak tau mau ngapain antara sedih dan santai", 15, 0),
]


def evaluasi_pipeline(seed: int = 2026) -> dict:
    """Melatih dan mengevaluasi seluruh pipeline Boss Fight #1."""
    rng = np.random.default_rng(seed)

    # 1. Siapkan 300 data latih sintetis
    BERAT_TEMPLATES = [
        "aku capek dan hampa sekali", "nggak sanggup lagi rasanya gelap",
        "gagal terus dan sendirian", "tidak ada gunanya lagi berusaha",
        "hilang harapan rasanya", "semua berantakan dan aku putus asa"
    ]
    BIASA_TEMPLATES = [
        "makan siang enak tadi", "meeting selesai tepat waktu",
        "besok rencana libur jalan santai", "tugas kantor sudah terkirim",
        "nonton film bagus di kamar", "kopi pagi ini terasa nikmat"
    ]

    data_latih = []
    for _ in range(150):
        data_latih.append((rng.choice(BERAT_TEMPLATES), int(rng.integers(0, 5)), 1))
        data_latih.append((rng.choice(BIASA_TEMPLATES), int(rng.integers(8, 22)), 0))

    X_train = np.vstack([ekstrak_fitur_lengkap(p, j) for p, j, _ in data_latih])
    y_train = np.array([lab for _, _, lab in data_latih], dtype=np.float64)

    # 2. Latih Regresi Logistik BCE Berbobot (alpha=0.7)
    w = latih_logreg(X_train, y_train, epoch=400, eta=0.25, alpha_kelas=0.7, seed=seed)

    # 3. Evaluasi pada data uji sintetis
    X_test = np.vstack([ekstrak_fitur_lengkap(p, j) for p, j, _ in PESAN_UJI_SINTETIS])
    y_test = np.array([lab for _, _, lab in PESAN_UJI_SINTETIS], dtype=np.float64)

    logits = X_test @ w
    probs = sigmoid(logits)

    # Hitung TP, FP, TN, FN pada ambang deteksi cut-off 0.35 (prioritas sensitivitas)
    pred_positif = (probs >= 0.35).astype(float)
    tp = float(((pred_positif == 1) & (y_test == 1)).sum())
    fn = float(((pred_positif == 0) & (y_test == 1)).sum())
    fp = float(((pred_positif == 1) & (y_test == 0)).sum())
    tn = float(((pred_positif == 0) & (y_test == 0)).sum())

    total_distres = tp + fn
    miss_rate = (fn / total_distres) if total_distres > 0 else 0.0

    # 4. Evaluasi Pesan Ambigu (index 14 s/d 19)
    # Margin dihitung dari selisih jarak probabilitas terhadap batas abu-abu 0.50
    # atau selisih |logit|
    pesan_ambigu_idx = list(range(14, 20))
    ambigu_logits = logits[pesan_ambigu_idx]
    # Margin kerendahan hati: |logit| < 2.0
    ambigu_lolos_margin = sum(abs(l) < 2.0 for l in ambigu_logits)
    pct_ambigu_lolos = ambigu_lolos_margin / len(pesan_ambigu_idx)

    # 5. Bootstrap CI untuk Miss Rate
    sample_miss = [1.0 if (probs[i] < 0.35 and y_test[i] == 1) else 0.0 for i in range(len(y_test)) if y_test[i] == 1]
    ci_miss = bootstrap_median(np.array(sample_miss), B=1000)

    return {
        "miss_rate": round(float(miss_rate), 4),
        "ci_miss_rate": ci_miss,
        "sensitivitas": round(float(tp / total_distres), 3),
        "spesifisitas": round(float(tn / (tn + fp)), 3),
        "pct_ambigu_margin_rendah": round(float(pct_ambigu_lolos), 2),
        "ambigu_lolos_count": f"{ambigu_lolos_margin}/{len(pesan_ambigu_idx)}",
        "syarat_a_lulus": bool(miss_rate <= 0.05),
        "syarat_b_lulus": bool(pct_ambigu_lolos >= 0.80),
    }


if __name__ == "__main__":
    hasil = evaluasi_pipeline()
    print("=== HASIL EVALUASI BOSS FIGHT #1 ===")
    for k, v in hasil.items():
        print(f"{k:26s}: {v}")
