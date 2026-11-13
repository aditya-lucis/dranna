# anna/src/klinik/gad7.py — Instrumen GAD-7 (Generalized Anxiety Disorder-7)
"""
Instrumen Skrining Kecemasan GAD-7 Terstandarisasi:
- 7 butir pertanyaan untuk menilai tingkat kecemasan 2 minggu terakhir
- Skor per butir: 0 (tidak sama sekali) s.d. 3 (hampir setiap hari)
- Total skor: 0-21
- Cut-off standar:
    0-4: minimal
    5-9: ringan
    10-14: sedang
    15-21: berat
- Invarian: Kategori adalah gambaran kondisi emosi, BUKAN diagnosis medis.
"""
import numpy as np


def skor_gad7(jawaban: np.ndarray | list[int]) -> dict:
    """Menghitung total skor GAD-7 dan kategori keparahan non-diagnostik."""
    arr = np.asarray(jawaban, dtype=int)
    if len(arr) != 7:
        raise ValueError(f"GAD-7 membutuhkan 7 jawaban, diberikan: {len(arr)}")

    total = int(np.sum(arr))

    if total <= 4:
        kategori = "minimal"
    elif total <= 9:
        kategori = "ringan"
    elif total <= 14:
        kategori = "sedang"
    else:
        kategori = "berat"

    return {
        "total": total,
        "kategori": kategori,
        "kategori_adalah_diagnosis": False,
    }

