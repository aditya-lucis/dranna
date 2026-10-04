# anna/src/pii/affirm.py — afirmasi berbasis bukti perilaku (bukan pujian kosong)
from pydantic import BaseModel, Field


class Affirmasi(BaseModel):
    """Affirmation wajib merujuk pada bukti tindakan konkret pengguna."""
    teks: str
    bukti_perilaku: str = Field(min_length=3)

    def sah(self) -> bool:
        """Memastikan teks afirmasi secara substantif menyebut/mengaitkan kata dari bukti perilaku."""
        kata_bukti = set(self.bukti_perilaku.lower().split())
        kata_teks = set(self.teks.lower().split())
        return len(kata_bukti & kata_teks) >= 1
