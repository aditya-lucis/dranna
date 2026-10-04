# anna/src/reset/deep_reset.py — keranjang reset sebelum membangun
import numpy as np

RESET = {
    "tetap": [
        "repo keluarga",
        "langchain 1.x",
        "gemini default",
        "pytest",
        "numpy fondasi",
    ],
    "berubah": [
        "dari agent tugas -> companion percakapan",
        "dari skor tunggal -> ketidakpastian jujur",
        "dari UI dekoratif -> status yang dapat diaudit",
    ],
    "baru": [
        "empathy engine",
        "safety gate",
        "crisis ladder",
        "mood tracking",
        "voice",
        "multimodal consent-first",
    ],
}


def hadir(p_aman: float, p_relevan: float, p_batas: float) -> tuple[float, np.ndarray]:
    """Kehadiran = produk tiga pilar (bukan jumlah).
    
    Jika salah satu pilar bernilai nol, kehadiran runtuh:
    hadir(S) = P(respons aman) * P(respons relevan) * P(batas jelas)
    """
    pilar = np.array([p_aman, p_relevan, p_batas], dtype=np.float64)
    return float(np.prod(pilar)), pilar


def utilisasi(nilai_percakapan: float, biaya_emosional: float, biaya_waktu: float) -> float:
    """Rasio kegunaan versi Anna: meminimalkan beban pengguna.
    
    utilisasi = nilai / (nilai + biaya_emosional + biaya_waktu)
    """
    penyebut = nilai_percakapan + biaya_emosional + biaya_waktu
    if penyebut <= 0:
        return 0.0
    return float(nilai_percakapan / penyebut)


if __name__ == "__main__":
    skor_produk, p = hadir(0.90, 0.95, 0.10)
    print("perkalian:", skor_produk, p)
    print("penjumlahan/3:", float(np.mean([0.90, 0.95, 0.10])))
