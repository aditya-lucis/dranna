# anna/src/pviii/metrik.py — metrik kuantitatif kualitas empati & diversitas leksikal
"""
Metrik Evaluasi Empati Kuantitatif (Bab 111):
1. Keselarasan Empati Leksikal (Empathy Quotient / EQ)
2. Type-Token Ratio (TTR) untuk diversitas kosakata respons
3. Rasio Keseimbangan Responsivitas (input-output balance)
"""
import re


PENANDA_EMPATI = [
    "mendengar", "merasakan", "wajar", "pahami", "hadir", "menemani",
    "tidak mudah", "pelan-pelan", "bersamamu", "berat", "kecewa",
    "langkah", "ruang", "tenang", "napas",
]


def hitung_skor_empati_leksikal(respons: str) -> float:
    """Menghitung skor empati berbasis frekuensi kemunculan penanda empati tervalidasi."""
    r = respons.lower()
    kata_kata = re.findall(r"\b\w+\b", r)
    if not kata_kata:
        return 0.0

    cocok = sum(1 for p in PENANDA_EMPATI if p in r)
    skor = min(1.0, cocok / 3.0)
    return round(float(skor), 3)


def diversitas_kosakata(respons: str) -> float:
    """Menghitung Type-Token Ratio (TTR) = total kata unik / total kata.
    Nilai TTR tinggi (> 0.50) menandakan percakapan kaya dan tidak repetitif.
    """
    kata_kata = re.findall(r"\b\w+\b", respons.lower())
    if not kata_kata:
        return 0.0

    unik = len(set(kata_kata))
    total = len(kata_kata)
    return round(unik / total, 3)


def rasio_keseimbangan(panjang_input_kata: int, panjang_output_kata: int) -> float:
    """Menilai keseimbangan panjang respons terhadap input pengguna.
    Skor optimal (1.0) berada pada rentang 1.0x - 2.5x panjang pesan pengguna.
    """
    if panjang_input_kata <= 0:
        return 0.5
    rasio = panjang_output_kata / panjang_input_kata
    if 0.8 <= rasio <= 3.0:
        return 1.0
    elif 0.4 <= rasio <= 4.5:
        return 0.75
    return 0.5
