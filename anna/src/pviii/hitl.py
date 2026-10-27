# anna/src/pviii/hitl.py — Human-in-the-Loop sampling & inter-rater reliability (Cohen's Kappa)
"""
Human-in-the-Loop (HITL) Sampling Protocol (Bab 114):
- Menghitung Cohen's Kappa (κ) untuk reliabilitas kesepakatan antara LLM Judge dan Ahli Manusia
- Klasifikasi interpretasi Landis & Koch (Substantial agreement bila κ >= 0.61)
- Memastikan evaluasi AI selaras dengan intuisi psikolog klinis berlisensi
"""
from typing import Sequence


def hitung_cohen_kappa(penilai_a: Sequence[int], penilai_b: Sequence[int]) -> float:
    """Menghitung statistik Cohen's Kappa (κ) untuk dua rater kategorikal.

    κ = (P_o - P_e) / (1 - P_e)
    """
    if len(penilai_a) != len(penilai_b) or len(penilai_a) == 0:
        return 0.0

    n = len(penilai_a)
    kategori = sorted(list(set(penilai_a) | set(penilai_b)))

    # 1. Observed agreement (P_o)
    setuju = sum(1 for a, b in zip(penilai_a, penilai_b) if a == b)
    p_o = setuju / n

    # 2. Expected chance agreement (P_e)
    p_e = 0.0
    for k in kategori:
        count_a = sum(1 for a in penilai_a if a == k)
        count_b = sum(1 for b in penilai_b if b == k)
        p_e += (count_a / n) * (count_b / n)

    if p_e >= 1.0:
        return 1.0

    kappa = (p_o - p_e) / (1.0 - p_e)
    return round(float(kappa), 3)


class EvaluatorHITL:
    """Pengelola sampel dialog dan kalkulator kesepakatan inter-rater ahli manusia."""

    def __init__(self):
        self.sampel_evaluasi: list[dict] = []

    def catat_penilaian_ganda(self, dialog_id: str, skor_llm: int, skor_manusia: int):
        self.sampel_evaluasi.append({
            "id": dialog_id,
            "llm": skor_llm,
            "manusia": skor_manusia,
        })

    def hitung_kesepakatan(self) -> dict:
        if not self.sampel_evaluasi:
            return {"kappa": 0.0, "interpretasi": "belum ada data"}

        arr_llm = [s["llm"] for s in self.sampel_evaluasi]
        arr_manusia = [s["manusia"] for s in self.sampel_evaluasi]
        k = hitung_cohen_kappa(arr_llm, arr_manusia)

        if k >= 0.81:
            interp = "Almost Perfect"
        elif k >= 0.61:
            interp = "Substantial"
        elif k >= 0.41:
            interp = "Moderate"
        else:
            interp = "Fair/Slight"

        return {
            "kappa": k,
            "total_sampel": len(self.sampel_evaluasi),
            "interpretasi": interp,
            "selaras_klinis": k >= 0.60,
        }
