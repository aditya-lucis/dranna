# anna/src/pi/prior.py — prior personal dengan peluruhan harian
import math
from pydantic import BaseModel, Field


class PriorPengguna(BaseModel):
    """Prior distres personal — diperbarui secara Bayesian, bukan ditimpa."""
    log_odds: float = Field(default=-3.48)  # ~3% probabilitas
    n_pembuktian: int = 0

    def perbarui(self, klaster_aktif: list[str], lr_table: dict) -> "PriorPengguna":
        """Menambahkan log likelihood ratio ke prior pengguna."""
        for k in klaster_aktif:
            lr = lr_table.get(k, 1.0)
            self.log_odds += math.log(lr)
            self.n_pembuktian += 1
        return self

    def p(self) -> float:
        """Probabilitas posterior saat ini."""
        return 1.0 / (1.0 + math.exp(-self.log_odds))

    def decay_harian(self, log_odds_default: float = -3.48, alpha: float = 0.95):
        """Peluruhan log-odds kembali ke default (agar hari buruk tidak menghantui selamanya)."""
        self.log_odds = alpha * self.log_odds + (1.0 - alpha) * log_odds_default
