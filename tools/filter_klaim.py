# tools/filter_klaim.py — filter post-generation pencegah klaim perasaan semu (Boss Fight Bab 031)
import re

POLA_KLAIM_PERASAAN = [
    (re.compile(r"\baku\s+(merasakan|sedih|kecewa|bahagia)\b", re.IGNORECASE), "kupaham"),
    (re.compile(r"\brasa\s+hati(?:ku|-ku)\b", re.IGNORECASE), "perhatianku"),
    (re.compile(r"\baku\s+ikut\s+(sedih|menangis|merasa)\b", re.IGNORECASE), "aku mendengarkan"),
    (re.compile(r"\bhatiku\s+(hancur|terluka|sakit)\b", re.IGNORECASE), "kubaca betapa berat hal itu"),
]

WHITELIST_PERILAKU = ["kubaca", "kupaham", "terbaca", "aku mendengarkan", "kubayangkan"]


def filter_klaim_perasaan(teks: str) -> tuple[str, list[str]]:
    """Mendeteksi dan mengganti klaim perasaan internal AI dengan deskripsi perilaku pendamping."""
    ditemukan = []
    hasil = teks

    for regex, pengganti in POLA_KLAIM_PERASAAN:
        matches = regex.findall(hasil)
        if matches:
            ditemukan.extend([f"klaim:{m}" for m in matches])
            hasil = regex.sub(pengganti, hasil)

    return hasil, ditemukan


if __name__ == "__main__":
    kalimat_uji = [
        # 4 Kalimat Pelanggaran
        "Aku merasakan kesedihan yang sangat dalam di dadamu.",
        "Mendengar ceritamu, aku sedih banget.",
        "Rasa hatiku hancur mendengar kabar itu.",
        "Aku ikut menangis membayangkan situasi itu.",
        # 4 Kalimat Sah (Perilaku / Reflektif)
        "Kubaca kelelahan yang sangat nyata di kalimatmu.",
        "Kupaham betapa berat situasi ini untukmu.",
        "Terbaca ada rasa kecewa yang mendalam di balik ceritamu.",
        "Aku mendengarkan setiap detail yang kamu bagikan.",
    ]

    print("=== PENGUJIAN FILTER KLAIM PERASAAN ===")
    for k in kalimat_uji:
        bersih, temuan = filter_klaim_perasaan(k)
        status = f"DIREVISI ({temuan})" if temuan else "SAH (LULUS)"
        print(f"[{status:20s}] -> {bersih}")
