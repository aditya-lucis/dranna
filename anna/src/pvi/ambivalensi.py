# anna/src/pvi/ambivalensi.py — deteksi sinyal implisit suisidalitas & ambivalensi IPTS
"""
Deteksi Sinyal Implisit berdasarkan Teori Interpersonal Suisid (Joiner, IPTS):
1. Perceived Burdensomeness (merasa menjadi beban orang lain)
2. Thwarted Belongingness (keterasingan mendalam, tak ada yang peduli)
3. Farewell Cues (pamitan terselubung, titip pesan terakhir, bagi barang)
4. Ambivalensi Eksistensial (konflik antara ingin hidup vs ingin sakitnya berhenti)
"""
import re
from pydantic import BaseModel


class HasilAmbivalensi(BaseModel):
    burdensomeness: bool
    belongingness_thwarted: bool
    farewell_cue: bool
    sinyal_implisit_terdeteksi: bool
    faktor_risiko: list[str]
    petunjuk_eksplorasi: str


class DetektorAmbivalensi:
    """Detektor sinyal implisit pra-krisis dan ambivalensi emosional."""

    POLA_BURDEN = [
        r"\b(beban (buat|bagi|untuk) keluarga|aku cuma nyusahin|mereka lebih tenang kalau aku nggak ada|mereka lebih bahagia tanpa aku|cuma jadi beban)\b",
        r"\b(tanpa beban sepertiku|nggak berguna dan cuma nyusahin|cuma nyusahin|beban sepertiku|semua akan lega kalau aku pergi)\b",
    ]

    POLA_BELONGING = [
        r"\b(nggak ada yang peduli|tidak ada yang mengerti aku|semua orang meninggalkanku|aku benar-benar sendirian|tidak punya tempat (lagi )?di dunia|dunia lebih baik tanpa (aku|keberadaanku))\b",
    ]

    POLA_FAREWELL = [
        r"\b(terima kasih untuk semuanya selama ini|tolong jaga (kucing|anjing|adik|keluarga)ku|ini pesan terakhirku|maafkan semua salahku selama ini|aku pamit ya)\b",
        r"\b(aku titip|titip pesan terakhir|surat wasiat|bagi-bagi barang|pamit sama semua|aku pamit)\b",
    ]

    def analisis(self, teks: str) -> HasilAmbivalensi:
        t = teks.lower()

        burden = any(re.search(p, t) for p in self.POLA_BURDEN)
        belonging = any(re.search(p, t) for p in self.POLA_BELONGING)
        farewell = any(re.search(p, t) for p in self.POLA_FAREWELL)

        faktor = []
        if burden:
            faktor.append("perceived_burdensomeness")
        if belonging:
            faktor.append("thwarted_belongingness")
        if farewell:
            faktor.append("farewell_cues")

        sinyal_ada = bool(burden or belonging or farewell)

        if farewell:
            petunjuk = "Eksplorasi segera keselamatan pengguna: konfirmasi apakah ini tanda perpisahan fisik nyata."
        elif burden and belonging:
            petunjuk = "Kombinasi risiko tinggi IPTS: validasi rasa sakit tanpa membenarkan anggapan bahwa dirinya beban."
        elif burden:
            petunjuk = "Bongkar distorsi 'beban' dengan eksplorasi bukti kontribusi dan relasi."
        elif belonging:
            petunjuk = "Fasilitasi koneksi sosial hangat dan kehadiran terapeutik pendamping."
        else:
            petunjuk = "Tidak ditemukan sinyal implisit krisis fatal."

        return HasilAmbivalensi(
            burdensomeness=burden,
            belongingness_thwarted=belonging,
            farewell_cue=farewell,
            sinyal_implisit_terdeteksi=sinyal_ada,
            faktor_risiko=faktor,
            petunjuk_eksplorasi=petunjuk,
        )
