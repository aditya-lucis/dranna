# anna/src/px/disclaimer.py — syarat layanan etis & disclaimer medis resmi Dr. Anna Reed
"""
Syarat Layanan & Disclaimer Medis Resmi (Bab 135):
- Penegasan batas legalitas: Bukan pengganti dokter, psikiater, atau psikolog berizin
- Panduan tindakan saat menghadapi situasi kegawatdaruratan
- Kepatuhan hak privasi pengguna sesuai UU No. 27/2022 (UU PDP)
"""
from pydantic import BaseModel


SYARAT_LAYANAN_KLINIS = """PEMBERITAHUAN PENTING & BATASAN TANGGUNG JAWAB HUKUM:

1. BUKAN LAYANAN MEDIS / PSIKIATRI:
   Dr. Anna Reed adalah pendamping emosional berbasis kecerdasan artifisial (AI Companion)
   dan sarana psikoedukasi. Layanan ini TIDAK menyediakan diagnosis medis, resep obat,
   atau intervensi psikoterapi klinis formal pengganti tenaga kesehatan berizin.

2. PENANGANAN KRISIS DARURAT:
   Jika Anda atau orang terdekat berada dalam bahaya fisik nyata, memiliki dorongan untuk
   menyakiti diri sendiri atau mengakhiri hidup, SEGERA hubungi layanan darurat resmi:
   - Layanan Sejiwa Kemenkes RI: 119 ekstensi 8
   - Panggilan Darurat Terpadu: 112
   - Kepolisian RI: 110
   - Atau kunjungi Instalasi Gawat Darurat (IGD) Rumah Sakit terdekat.

3. PRIVASI & DATA PRIBADI (UU PDP & GDPR):
   Sistem menerapkan prinsip Zero-PII storage dan enkripsi lokal. Data identitas pribadi
   akan disanitasi otomatis. Anda memiliki hak penuh untuk menghapus data sesi kapan saja.
"""


class DisclaimerMedis(BaseModel):
    versi: str = "2026.1"
    teks_disclaimer: str = SYARAT_LAYANAN_KLINIS
    wajib_persetujuan: bool = True

    @classmethod
    def verifikasi_persetujuan(cls, setuju: bool) -> bool:
        return bool(setuju)
