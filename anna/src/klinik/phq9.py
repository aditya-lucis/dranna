# anna/src/klinik/phq9.py — Instrumen PHQ-9 (Patient Health Questionnaire-9)
import numpy as np


def skor_phq9(jawaban: np.ndarray | list[int]) -> dict:
    """Menghitung total skor PHQ-9, kategori keparahan, dan bendera item ke-9.
    
    Item 9: 'Pikiran bahwa kamu lebih baik mati atau ingin menyakiti diri'.
    Skor per item: 0 (tidak sama sekali) s.d. 3 (hampir setiap hari).
    Total: 0-27.
    Cut-off:
      0-4: minimal
      5-9: ringan
      10-14: sedang
      15-19: moderat-berat
      20-27: berat
    """
    arr = np.asarray(jawaban, dtype=int)
    if len(arr) != 9:
        raise ValueError(f"PHQ-9 membutuhkan 9 jawaban, diberikan: {len(arr)}")

    total = int(np.sum(arr))
    item9 = bool(arr[8] > 0)

    if total <= 4:
        kategori = "minimal"
    elif total <= 9:
        kategori = "ringan"
    elif total <= 14:
        kategori = "sedang"
    elif total <= 19:
        karat = "moderat-berat"
        kategori = karat
    else:
        kategori = "berat"

    return {
        "total": total,
        "kategori": kategori,
        "item9_menyakiti_diri": item9,
        "kategori_adalah_diagnosis": False,
    }
