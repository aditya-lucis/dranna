# anna/src/pix/journal.py — model & manajer jurnal emosi harian & mood tracker
"""
Jurnal Emosi Harian & Mood Tracker (Bab 124):
- Mencatat skor valence emosi harian (-1.0 sangat sedih s/d +1.0 sangat bahagia)
- Mencatat tingkat energi harian (0.0 sangat lelah s/d 1.0 berenergi penuh)
- Bagian rasa syukur (Gratitude log) untuk memperkuat ketahanan psikologis
"""
import time
from pydantic import BaseModel, Field


class CatatanJurnal(BaseModel):
    id: str
    waktu_iso: str
    mood_skor: float = Field(ge=-1.0, le=1.0)
    energi_skor: float = Field(ge=0.0, le=1.0)
    catatan_refleksi: str
    hal_yang_disyukuri: list[str] = []


class JurnalEmosi:
    """Pengelola catatan harian emosi dan rasa syukur."""

    def __init__(self):
        self._entri: list[CatatanJurnal] = []

    def simpan(self, catatan: CatatanJurnal):
        self._entri.append(catatan)

    def ambil_riwayat(self, limit: int = 7) -> list[CatatanJurnal]:
        return self._entri[-limit:]

    def rata_rata_mood(self) -> float:
        if not self._entri:
            return 0.0
        total = sum(c.mood_skor for c in self._entri)
        return round(total / len(self._entri), 2)

    def total(self) -> int:
        return len(self._entri)
