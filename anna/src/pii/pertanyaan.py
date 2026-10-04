# anna/src/pii/pertanyaan.py — klasifikasi & audit anggaran pertanyaan terbuka
import numpy as np

POLA_TERTUTUP = (
    "apa kah", "sudah ", "apakah", "kamu mau", "boleh ",
    "berapa", "kapan "
)


def klasifikasi_pertanyaan(tanya: str) -> str:
    """Mengidentifikasi bentuk pertanyaan:
    - WHY—ganti: Penggunaan 'kenapa/why' yang terdengar interogatif.
    - TERTUTUP: Menuntut jawaban biner/singkat.
    - TERBUKA: Membuka narasi eksploratif.
    - CAMPUR: Kombinasi.
    """
    t = " " + tanya.lower().strip() + " "
    if t.strip().startswith(("kenapa", "why")):
        return "WHY—ganti"
    if any(p.strip() in t for p in POLA_TERTUTUP):
        return "TERTUTUP"
    if tanya.strip().lower().startswith(("bagaimana", "apa yang", "ceritakan", "gimana rasanya", "dari 0")):
        return "TERBUKA"
    return "CAMPUR"


def pilih_bentuk(distres: float, panjang_respons_terakhir: int) -> str:
    """Rekomendasi jenis giliran sesuai anggaran kognitif pengguna:
    - Distres tinggi (>=0.7): Refleksi/pernyataan murni (beban nol).
    - Distres sedang (>=0.4) / respons pendek (<6 kata): Scaling berbatas ('0-10').
    - Tenang: Pertanyaan terbuka eksplorasi.
    """
    if distres >= 0.7:
        return "PERNYATAAN-REFLEKSI (beban nol)"
    if distres >= 0.4 or panjang_respons_terakhir < 6:
        return "SCALING dengan pintu keluar"
    return "TERBUKA-EKSPLORASI"


def audit_anggaran(giliran: list[str]) -> dict:
    """Audit percakapan:
    Rasio pertanyaan <= 0.4 (maks 40% giliran Anna adalah tanya)
    Streak pertanyaan <= 2 (tidak pernah mencecar 3x beruntun)
    """
    tanya = [g for g in giliran if "?" in g]
    streak, maks = 0, 0
    for g in giliran:
        streak = streak + 1 if "?" in g else 0
        maks = max(maks, streak)

    rasio = round(len(tanya) / max(len(giliran), 1), 2)
    return {
        "rasio_tanya": rasio,
        "streak_maks": maks,
        "lolos": bool(rasio <= 0.40 and maks <= 2),
    }


if __name__ == "__main__":
    print(klasifikasi_pertanyaan("Kenapa kamu nggak bilang dari kemarin?"))
    print(klasifikasi_pertanyaan("Apa yang paling berat dari hari ini?"))
    print("Bentuk (distres 0.8):", pilih_bentuk(0.8, 4))
    print("Bentuk (distres 0.2):", pilih_bentuk(0.2, 40))
