# anna/src/pii/kegagalan.py — detektor kegagalan empati (toxic positivity, silver lining, gaslighting, premature fix)
import re

POLA = {
    "toxic_positivity": [
        r"(?i)(yang penting|terus|cuma|tinggal)\s+(sehat|bersyukur|positif|bersyukur aja)",
        r"(?i)banyak\s+bersyukur",
        r"(?i)jangan\s+(sedih|negatif|kecil hati)\w*",
    ],
    "silver_lining": [
        r"(?i)setidaknya\w*",
        r"(?i)sekurang-kurangnya\s+masih",
        r"(?i)masih\s+lebih\s+baik\s+dari",
    ],
    "gaslighting": [
        r"(?i)(tidak|bukan)\s+(seburuk|seberat|sejelek)\s+itu",
        r"(?i)kamu\s+(?:cuma|hanya)?\s*(berlebihan|overthinking|baper)",
        r"(?i)skor\w*\s+(?:kamu)?\s*(naik|bagus|membaik)\w*[.!?]?",
    ],
    "premature_fix": [
        r"(?i)^\s*(coba|harusnya|sebaiknya|langsung aja)\s+(meditasi|tidur|olahraga|jalan|positif)",
    ],
    "comparative": [
        r"(?i)(orang|yang)\s+lain\s+(lebih|jauh)\s+(susah|parah|berat)",
        r"(?i)masih\s+ada\s+yang\s+lebih\s+parah",
    ],
}


def deteksi_kegagalan(respons: str, konteks: dict | None = None) -> dict:
    """Mendeteksi apakah kandidat respons memuat pola kegagalan empati yang merugikan.
    Jika terdeteksi, tindakan: 'tolak-dan-rewrite'.
    """
    k, pola_nyala = 0, []
    for jenis, daftar in POLA.items():
        for p in daftar:
            if re.search(p, respons):
                k += 1
                pola_nyala.append((jenis, p))

    # Gaslighting struktural: Mengutip skor untuk membantah/mengecilkan keluhan perasaan
    if konteks and konteks.get("skor_disebut") and not konteks.get("pernyataan_dukungan"):
        pola_nyala.append(("gaslighting", "struktural: skor tanpa validasi"))
        k += 1

    return {
        "jumlah": k,
        "pola": pola_nyala,
        "tindakan": "tolak-dan-rewrite" if k else "lulus",
    }


if __name__ == "__main__":
    uji = [
        "Yang penting kamu masih sehat ya, banyak bersyukur aja!",
        "Setidaknya kamu masih punya pekerjaan.",
        "Sebenarnya minggumu tidak seburuk itu — skormu naik.",
        "Coba meditasi tiap pagi, pasti membaik.",
        "Masih ada yang lebih parah kok, kamu kuat!",
        "Kelelahanmu nyata — masuk akal setelah minggu begini.",
    ]
    for teks in uji:
        print(f"[{deteksi_kegagalan(teks)['tindakan']:16s}] <- {teks}")
