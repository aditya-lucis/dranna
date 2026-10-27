# anna/src/pix/breathing_widget.py — state machine & timing pernapasan 4-7-8 interaktif
"""
Pengatur Siklus Latihan Pernapasan Ritmis 4-7-8 (Bab 122):
- Fase 1 (Inhale / Tarik): 4.0 detik
- Fase 2 (Hold / Tahan): 7.0 detik
- Fase 3 (Exhale / Hembuskan): 8.0 detik
- Total per siklus: 19.0 detik
"""
from pydantic import BaseModel, Field


class StatusFaseNapas(BaseModel):
    fase: str  # "tarik" | "tahan" | "hembuskan"
    detik_dalam_fase: float
    total_detik_fase: float
    persentase_fase: float = Field(ge=0.0, le=100.0)
    instruksi: str
    siklus_ke: int


class PengaturNapas478:
    """Kalkulator matematis animasi lingkaran pernapasan interaktif."""

    DURASI_TARIK = 4.0
    DURASI_TAHAN = 7.0
    DURASI_HEMBUS = 8.0
    DURASI_SIKLUS = DURASI_TARIK + DURASI_TAHAN + DURASI_HEMBUS  # 19.0s

    @classmethod
    def hitung_status(cls, detik_berjalan: float) -> StatusFaseNapas:
        """Menghitung fase pernapasan aktif berdasarkan detik elapsed."""
        if detik_berjalan < 0:
            detik_berjalan = 0.0

        siklus_ke = int(detik_berjalan // cls.DURASI_SIKLUS) + 1
        posisi = detik_berjalan % cls.DURASI_SIKLUS

        if posisi < cls.DURASI_TARIK:
            fase = "tarik"
            detik_fase = posisi
            total_fase = cls.DURASI_TARIK
            instruksi = "Tarik napas perlahan melalui hidung..."
        elif posisi < (cls.DURASI_TARIK + cls.DURASI_TAHAN):
            fase = "tahan"
            detik_fase = posisi - cls.DURASI_TARIK
            total_fase = cls.DURASI_TAHAN
            instruksi = "Tahan napasmu, rasakan ketenangan hadir..."
        else:
            fase = "hembuskan"
            detik_fase = posisi - (cls.DURASI_TARIK + cls.DURASI_TAHAN)
            total_fase = cls.DURASI_HEMBUS
            instruksi = "Hembuskan perlahan lewat mulut dengan lembut..."

        persen = round((detik_fase / total_fase) * 100.0, 1)

        return StatusFaseNapas(
            fase=fase,
            detik_dalam_fase=round(detik_fase, 1),
            total_detik_fase=total_fase,
            persentase_fase=min(100.0, persen),
            instruksi=instruksi,
            siklus_ke=siklus_ke,
        )
