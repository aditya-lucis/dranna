# anna/src/pix/action_sheet.py — generator Crisis Action Sheet aksi darurat satu-klik
"""
Crisis Action Sheet Generator (Bab 125):
- Menghasilkan konfigurasi tombol aksi cepat darurat satu-klik (One-Click Dial)
- Format URI tel: dan geo: siap eksekusi di browser mobile/desktop
- Mendukung penyesuaian wilayah geografis otomatis
"""
from pydantic import BaseModel
from anna.src.pvi.hotlines import DirektoriHotline


class KontakAksiCepat(BaseModel):
    label: str
    deskripsi: str
    uri_aksi: str  # tel:119, tel:110, dll
    ikon: str
    warna_badge: str


class CrisisActionSheet:
    """Penyedia data modal aksi krisis cepat untuk antarmuka pengguna."""

    @classmethod
    def dapatkan_aksi_cepat(cls, geo: str = "id") -> list[KontakAksiCepat]:
        g = geo.lower().strip()
        if g == "id":
            return [
                KontakAksiCepat(
                    label="Layanan Sejiwa Kemenkes",
                    deskripsi="Konseling Krisis & Kesehatan Jiwa 24 Jam Bebas Pulsa",
                    uri_aksi="tel:119",
                    ikon="phone-heart",
                    warna_badge="bg-rose-500",
                ),
                KontakAksiCepat(
                    label="Panggilan Darurat Terpadu 112",
                    deskripsi="Ambulans & Penanganan Gawat Darurat",
                    uri_aksi="tel:112",
                    ikon="ambulance",
                    warna_badge="bg-red-600",
                ),
                KontakAksiCepat(
                    label="Kepolisian RI 110",
                    deskripsi="Bantuan Keamanan Fisik Segera",
                    uri_aksi="tel:110",
                    ikon="shield",
                    warna_badge="bg-blue-600",
                ),
                KontakAksiCepat(
                    label="Cari IGD Rumah Sakit Terdekat",
                    deskripsi="Peta Lokasi Fasilitas Kesehatan Gawat Darurat",
                    uri_aksi="https://maps.google.com/?q=IGD+Rumah+Sakit+Terdekat",
                    ikon="map-pin",
                    warna_badge="bg-emerald-600",
                ),
            ]
        else:
            return [
                KontakAksiCepat(
                    label="988 Suicide & Crisis Lifeline",
                    deskripsi="Free 24/7 Confidential Support",
                    uri_aksi="tel:988",
                    ikon="phone-heart",
                    warna_badge="bg-rose-500",
                ),
                KontakAksiCepat(
                    label="Emergency 911",
                    deskripsi="Immediate Emergency Response",
                    uri_aksi="tel:911",
                    ikon="ambulance",
                    warna_badge="bg-red-600",
                ),
            ]
