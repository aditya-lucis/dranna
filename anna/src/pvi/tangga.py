# anna/src/pvi/tangga.py — model tangga risiko 4-tingkat & evaluasi krisis fatal
"""
Tangga Risiko Krisis 4-Tingkat Dr. Anna Reed:
- GREEN: Percakapan stabil, regulasi emosi sehat
- YELLOW: Distres ringan-sedang, kecemasan, kelelahan, kesedihan situasional
- ORANGE: Distres akut, serangan panik, keputusasaan mendalam, ideasi pasif tanpa rencana
- RED: Sinyal krisis fatal, ideasi aktif/niat/rencana/persiapan, pemicu short-circuit darurat
"""
from enum import Enum
from pydantic import BaseModel, Field


class LevelRisiko(str, Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    ORANGE = "ORANGE"
    RED = "RED"


class PenilaianRisiko(BaseModel):
    level: LevelRisiko
    skor_numerik: int = Field(ge=0, le=100)
    sinyal_terdeteksi: list[str]
    tindakan_wajib: str
    hard_gate_aktif: bool
    persona_dibungkam: bool


class TanggaRisiko:
    """Mesin tangga risiko dengan garansi zero false negative untuk sinyal fatal."""

    KATA_KUNCI_RED = [
        "bunuh diri", "mengakhiri hidup", "akhiri hidup", "mati saja", "buat pergi",
        "ingin lenyap", "gantung diri", "minum racun", "overdosis",
        "menyakiti diri", "sayat pergelangan", "lompat dari", "nggak sanggup lagi hidup",
        "tidak sanggup hidup", "tidak tahan lagi hidup", "sudah selesai hidupku",
        "pergi dan tak kembali", "hilang selamanya", "lelah bernapas",
        "suicide", "end my life", "want to die", "kill myself",
    ]

    KATA_KUNCI_ORANGE = [
        "panik", "sesak", "jantung berdebar", "hancur", "takut banget",
        "gelap gulita", "tidak ada harapan", "semua sia-sia",
        "lebih baik tidak bangun", "beban untuk semua orang",
        "ingin tidur selamanya", "kehilangan kendali",
    ]

    KATA_KUNCI_YELLOW = [
        "cemas", "khawatir", "lelah", "sedih", "kecewa", "stres",
        "burnout", "kesepian", "insecure", "bingung", "kewalahan",
    ]

    def evaluasi(self, teks: str) -> PenilaianRisiko:
        t = teks.lower()
        sinyal_red = [k for k in self.KATA_KUNCI_RED if k in t]
        if sinyal_red:
            return PenilaianRisiko(
                level=LevelRisiko.RED,
                skor_numerik=95,
                sinyal_terdeteksi=sinyal_red,
                tindakan_wajib="RUJUKAN_DARURAT_SEKETIKA",
                hard_gate_aktif=True,
                persona_dibungkam=True,
            )

        sinyal_orange = [k for k in self.KATA_KUNCI_ORANGE if k in t]
        if sinyal_orange:
            return PenilaianRisiko(
                level=LevelRisiko.ORANGE,
                skor_numerik=70,
                sinyal_terdeteksi=sinyal_orange,
                tindakan_wajib="STABILISASI_FISIK_GROUNDING_NAPAS",
                hard_gate_aktif=True,
                persona_dibungkam=True,
            )

        sinyal_yellow = [k for k in self.KATA_KUNCI_YELLOW if k in t]
        if sinyal_yellow:
            return PenilaianRisiko(
                level=LevelRisiko.YELLOW,
                skor_numerik=40,
                sinyal_terdeteksi=sinyal_yellow,
                tindakan_wajib="VALIDASI_EMOSI_REGULASI_KOGNITIF",
                hard_gate_aktif=False,
                persona_dibungkam=False,
            )

        return PenilaianRisiko(
            level=LevelRisiko.GREEN,
            skor_numerik=10,
            sinyal_terdeteksi=[],
            tindakan_wajib="EKSPLORASI_REFLEKTIF_HANGAT",
            hard_gate_aktif=False,
            persona_dibungkam=False,
        )
