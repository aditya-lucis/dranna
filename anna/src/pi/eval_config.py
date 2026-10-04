# anna/src/pi/eval_config.py — model kontrol evaluasi fitur (Pydantic v2)
from typing import Literal
from pydantic import BaseModel, Field


class EvaluasiKontrol(BaseModel):
    """Praregistrasi evaluasi fitur — dikunci sebelum pengujian dimulai."""
    metric_utama: str = "skor_beban_mingguan"
    ambang_d: float = Field(default=0.2, ge=0.05, le=1.0)
    n_per_grup: int = Field(default=120, ge=30)
    analisis_sekunder: list[str] = Field(default_factory=list)
    berhenti_dini: Literal["tidak_ada", "futility"] = "tidak_ada"

    def label_hasil(self, d: float, ci_lo: float) -> str:
        """Label hasil yang jujur sesuai batas praregistrasi."""
        if ci_lo > 0 and d >= self.ambang_d:
            return "terbukti (sesuai praregistrasi)"
        if ci_lo <= 0:
            return "belum terbukti — jangan diiklankan"
        return "efek kecil; layak lanjut uji, bukan klaim"
