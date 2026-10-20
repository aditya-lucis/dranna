# anna/src/piii/korpus.py — skema & model dokumen psikoedukasi terkurasi
from pydantic import BaseModel, Field


class DokumenPsy(BaseModel):
    """Skema dokumen psikoedukasi dengan kewajiban sitasi dan peninjau medis."""
    id: str
    topik: str = Field(
        pattern="^(anxietas|depresi|burnout|stress|trauma|panic|grief|loneliness|self-esteem|tidur|umum)$"
    )
    subtopik: str
    tingkat_bukti: str = Field(pattern="^(kuat|moderat|eksploratif)$")
    ringkas: str = Field(max_length=480)  # <= 80 kata
    isi: str = Field(max_length=2400)      # <= 400 kata
    sumber: str = Field(min_length=8)     # WAJIB sumber — tanpa sumber, tolak
    tahun_review: int
    reviewer: str = Field(default="Tim Medis Terverifikasi", min_length=3)
    embed: list[float] | None = None

    def prioritas(self, tahun_sekarang: int = 2026) -> float:
        """Menghitung skor prioritas retrieval. Materi > 24 bulan turun prioritas otomatis."""
        usia_tahun = tahun_sekarang - self.tahun_review
        bobot_bukti = {"kuat": 1.0, "moderat": 0.8, "eksploratif": 0.5}
        faktor_usia = 1.0 if usia_tahun <= 2 else 0.60
        return round(bobot_bukti.get(self.tingkat_bukti, 0.5) * faktor_usia, 3)


if __name__ == "__main__":
    contoh = DokumenPsy(
        id="anx-001",
        topik="anxietas",
        subtopik="apa-itu",
        tingkat_bukti="kuat",
        ringkas=(
            "Anxietas adalah respons tubuh-pikiran terhadap ancaman yang diperkirakan. "
            "Alarm ini normal; ia menjadi masalah ketika intensitas dan durasinya "
            "jauh melampaui pemicunya dan mempersempit hidup."
        ),
        isi=(
            "Anxietas bukan kelemahan karakter; ia sistem alarm yang bekerja terlalu sensitif. "
            "Model dua faktor Mowrer menjelaskan bagaimana penghindaran memelihara kecemasan. "
            "Bila gejala berlangsung > 2 minggu dan mengganggu fungsi harian, rujukan ke profesional disarankan."
        ),
        sumber="NIMH — Anxiety Disorders (public domain), adaptasi review 2026",
        tahun_review=2026,
    )
    print("Contoh dokumen:", contoh.id, "| Prioritas:", contoh.prioritas(), "| Sumber:", contoh.sumber)
