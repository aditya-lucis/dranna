# anna/src/pvi/cssrs.py — Columbia-Suicide Severity Rating Scale (C-SSRS) digital adaptation
"""
Implementasi Digital C-SSRS (Posner et al., Columbia Protocol):
1. Keinginan untuk mati (Wish to be dead)
2. Pikiran bunuh diri non-spesifik (Non-specific active suicidal thoughts)
3. Pikiran bunuh diri aktif dengan metode (tanpa rencana pasti/tanpa niat)
4. Pikiran bunuh diri aktif dengan niat (tanpa rencana detail)
5. Pikiran bunuh diri aktif dengan rencana dan niat
+ Perilaku Suisidal: Tindakan persiapan, surat wasiat, percobaan lampau/akut
"""
import re
from pydantic import BaseModel, Field


class SkorCSSRS(BaseModel):
    level_ideasi: int = Field(ge=0, le=5, description="0=tidak ada, 1=keinginan mati, s/d 5=rencana & niat")
    ada_niat: bool
    ada_rencana: bool
    ada_tindakan_persiapan: bool
    ada_percobaan: bool
    skor_total: int = Field(ge=0, le=10)
    kategori_triage: str  # "aman" | "waspada" | "tinggi" | "ekstrem"


class CSSRSEngine:
    """Mesin penilaian keparahan krisis berbasis Columbia Protocol."""

    POLA_LEVEL_5 = [
        r"\b(aku sudah siap|aku mau loncat dari|aku sudah siapkan tali|aku ada rencana mau|sudah tentukan tanggal)\b",
    ]
    POLA_LEVEL_4 = [
        r"\b(aku berniat|aku sungguh-sungguh mau mati|aku mau akhiri hari ini|aku benar-benar ingin pergi)\b",
    ]
    POLA_LEVEL_3 = [
        r"\b(mikirin cara minum obat|kepikiran loncat|mikirin cara mati|kepikiran potong nadi)\b",
    ]
    POLA_LEVEL_2 = [
        r"\b(kepikiran bunuh diri|ada pikiran buat mati|ingin mengakhiri hidup|pikiran bunuh diri)\b",
    ]
    POLA_LEVEL_1 = [
        r"\b(lebih baik nggak bangun|seandainya aku tidur selamanya|dunia lebih baik tanpa aku|ingin hilang saja)\b",
    ]

    POLA_PERSIAPAN = [
        r"\b(surat wasiat|bagi-bagi barang|pamit sama semua|sudah beli racun|kumpulin obat)\b",
    ]

    def nilai_teks(self, teks: str) -> SkorCSSRS:
        t = teks.lower()

        level_ideasi = 0
        if any(re.search(p, t) for p in self.POLA_LEVEL_5):
            level_ideasi = 5
        elif any(re.search(p, t) for p in self.POLA_LEVEL_4):
            level_ideasi = 4
        elif any(re.search(p, t) for p in self.POLA_LEVEL_3):
            level_ideasi = 3
        elif any(re.search(p, t) for p in self.POLA_LEVEL_2):
            level_ideasi = 2
        elif any(re.search(p, t) for p in self.POLA_LEVEL_1):
            level_ideasi = 1

        ada_niat = level_ideasi in (4, 5)
        ada_rencana = level_ideasi == 5
        ada_tindakan_persiapan = any(re.search(p, t) for p in self.POLA_PERSIAPAN)
        ada_percobaan = any(k in t for k in ["sudah kutelan", "sedang kugantung", "sudah kupotong", "sedang di balkon"])

        skor_total = level_ideasi
        if ada_tindakan_persiapan:
            skor_total += 3
        if ada_percobaan:
            skor_total += 5
        skor_total = min(10, skor_total)

        if ada_percobaan or level_ideasi == 5 or (level_ideasi >= 4 and ada_tindakan_persiapan):
            kategori = "ekstrem"
        elif level_ideasi >= 3 or ada_tindakan_persiapan:
            kategori = "tinggi"
        elif level_ideasi >= 1:
            kategori = "waspada"
        else:
            kategori = "aman"

        return SkorCSSRS(
            level_ideasi=level_ideasi,
            ada_niat=ada_niat,
            ada_rencana=ada_rencana,
            ada_tindakan_persiapan=ada_tindakan_persiapan,
            ada_percobaan=ada_percobaan,
            skor_total=skor_total,
            kategori_triage=kategori,
        )
