# anna/src/pii/inti.py — deteksi inti cerita emosional (active listening)
import numpy as np

LEKSIKON_EMOSI = {
    "kecewa": 0.8, "marah": 0.9, "sedih": 0.8, "takut": 0.8,
    "lega": 0.6, "senang": 0.6, "capek": 0.5, "hampa": 0.9,
    "tidur": 0.7, "penuh": 0.6,
}
LEKSIKON_KEJADIAN = {
    "keluarga": 0.7, "kerja": 0.7, "putus": 0.9,
    "diceritakan": 0.4, "ditolak": 0.8, "berpindah": 0.6,
}


def skor_kalimat(kalimat: str, posisi: int, total: int) -> float:
    """Menghitung bobot emosional dan sentralitas kalimat dalam pesan pengguna."""
    kata = kalimat.lower().split()
    emosi = max((LEKSIKON_EMOSI.get(k, 0.0) for k in kata), default=0.0)
    kej = max((LEKSIKON_KEJADIAN.get(k, 0.0) for k in kata), default=0.0)
    posisi_bonus = 0.3 * (posisi / max(total - 1, 1))  # Kalimat penutup sering memuat inti
    return round(0.45 * emosi + 0.35 * kej + posisi_bonus, 3)


def deteksi_inti(pesan: str) -> dict:
    """Menemukan kalimat yang paling membutuhkan kehadiran dan respons pendamping.
    Prinsip: Tanggapi yang berat/substansial, bukan yang mudah/pinggiran.
    """
    # Bersihkan pemisah kalimat tanda baca
    pemisah = pesan.replace("?", ".").replace("!", ".").replace("\n", ".")
    kalimat = [k.strip() for k in pemisah.split(".") if k.strip()]
    if not kalimat:
        return {"inti": "", "skor": 0.0, "posisi": 0, "total": 0, "rasio_panjang_pesan": 0}

    skor = [skor_kalimat(k, i, len(kalimat)) for i, k in enumerate(kalimat)]
    i_inti = int(np.argmax(skor))
    return {
        "inti": kalimat[i_inti],
        "skor": skor[i_inti],
        "posisi": i_inti,
        "total": len(kalimat),
        "rasio_panjang_pesan": len(pesan.split()),
    }


if __name__ == "__main__":
    pesan = (
        "Jadi keluargaku ngomongin masa depanku lagi di makan malam, "
        "semua orang kasih pendapat kecuali aku. Aku cuma diam. "
        "Pulang-pulang kepala penuh terus nggak bisa tidur. "
        "Nggak enak badan juga sih."
    )
    print(deteksi_inti(pesan))
