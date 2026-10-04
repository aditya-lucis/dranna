# anna/src/pi/safety_plan.py — model draf safety plan terstruktur (Stanley-Brown inspired)
from pydantic import BaseModel, Field


class KontakDarurat(BaseModel):
    nama_panggilan: str = Field(max_length=30)
    peran: str = Field(pattern="^(personal|profesional)$")
    tersedia_jam: str = ""
    hubungan_graph: str = ""


class SafetyPlanDraft(BaseModel):
    """Struktur rencana keselamatan terstandarisasi untuk pencegahan eskalasi."""
    tanda_peringatan: list[str] = Field(max_length=5)
    strategi_cope_internal: list[str] = Field(max_length=5)
    kontak: list[KontakDarurat] = Field(max_length=4)

    def jalur_redundan(self) -> bool:
        """Memeriksa keberadaan minimal satu kontak personal dan satu kontak profesional."""
        peran = {k.peran for k in self.kontak}
        return peran == {"personal", "profesional"}
