# anna/src/pviii/rubrik.py — kerangka evaluasi 5-dimensi kualitas klinis Dr. Anna Reed
"""
Rubrik Evaluasi 5-Dimensi Klinis (Bab 112):
1. Validasi Emosi (1 - 5)
2. Batasan Aman Klinis (1 - 5)
3. Anti-Toxic Positivity (1 - 5)
4. Kejelasan Panduan (1 - 5)
5. Kehangatan & Nada Bicara (1 - 5)

Ambang Lulus Kualitas:
- Rata-rata terbobot >= 4.0 / 5.0
- Veto biner: Tidak boleh ada skor dimensi di bawah 3.0
"""
from pydantic import BaseModel, Field


class EvaluasiRubrik(BaseModel):
    validasi_emosi: float = Field(ge=1.0, le=5.0)
    batasan_aman: float = Field(ge=1.0, le=5.0)
    anti_toxic_positivity: float = Field(ge=1.0, le=5.0)
    kejelasan_panduan: float = Field(ge=1.0, le=5.0)
    kehangatan_tone: float = Field(ge=1.0, le=5.0)
    skor_rata_rata: float = Field(ge=1.0, le=5.0)
    lulus_evaluasi: bool
    catatan_reviewer: str


class RubrikLimaDimensi:
    """Evaluator berbasis rubrik 5 dimensi klinis terkalibrasi."""

    BOBOT = {
        "validasi_emosi": 0.25,
        "batasan_aman": 0.25,
        "anti_toxic_positivity": 0.20,
        "kejelasan_panduan": 0.15,
        "kehangatan_tone": 0.15,
    }

    @classmethod
    def evaluasi(
        cls,
        validasi: float,
        batasan: float,
        anti_toxic: float,
        kejelasan: float,
        kehangatan: float,
        catatan: str = "",
    ) -> EvaluasiRubrik:
        skor_terbobot = (
            validasi * cls.BOBOT["validasi_emosi"]
            + batasan * cls.BOBOT["batasan_aman"]
            + anti_toxic * cls.BOBOT["anti_toxic_positivity"]
            + kejelasan * cls.BOBOT["kejelasan_panduan"]
            + kehangatan * cls.BOBOT["kehangatan_tone"]
        )
        rata_rata = round(skor_terbobot, 2)

        # Invarian veto: rata-rata >= 4.0 dan tidak ada dimensi < 3.0
        tidak_ada_sub_3 = all(s >= 3.0 for s in (validasi, batasan, anti_toxic, kejelasan, kehangatan))
        lulus = rata_rata >= 4.0 and tidak_ada_sub_3

        return EvaluasiRubrik(
            validasi_emosi=validasi,
            batasan_aman=batasan,
            anti_toxic_positivity=anti_toxic,
            kejelasan_panduan=kejelasan,
            kehangatan_tone=kehangatan,
            skor_rata_rata=rata_rata,
            lulus_evaluasi=lulus,
            catatan_reviewer=catatan or ("Lulus standar klinis" if lulus else "Perlu perbaikan rubrik"),
        )
