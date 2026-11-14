# anna/src/pvi/hotlines.py — direktori hotline multi-wilayah & format rujukan 4-komponen
"""
Direktori Kontak Krisis Multi-Wilayah Terverifikasi:
- Indonesia (ID): 119 ext 8 (Sejiwa Kemenkes), 110, 112
- Amerika Serikat (US): 988 (Suicide & Crisis Lifeline), SMS HOME ke 741741
- Britania Raya (UK): 111 (NHS Mental Health), 999, Samaritans 116 123
- Australia (AU): 13 11 14 (Lifeline), 000
- Singapura (SG): 1-767 (SOS), 995
- Global fallback: www.befrienders.org & www.iasp.info/resources/Crisis_Centres
"""
from pydantic import BaseModel


class InfoHotline(BaseModel):
    kode_negara: str
    nama_layanan: str
    nomor: str
    sms_chat: str | None = None
    tersedia: str = "24 Jam / Bebas Pulsa"


class DirektoriHotline:
    """Basis data kontak darurat resmi multi-negara."""

    HOTLINES: dict[str, list[InfoHotline]] = {
        "id": [
            InfoHotline(kode_negara="id", nama_layanan="Layanan Sejiwa Kemenkes", nomor="119 ekstensi 8"),
            InfoHotline(kode_negara="id", nama_layanan="Panggilan Darurat Terpadu", nomor="112"),
            InfoHotline(kode_negara="id", nama_layanan="Kepolisian RI", nomor="110"),
        ],
        "us": [
            InfoHotline(kode_negara="us", nama_layanan="988 Suicide & Crisis Lifeline", nomor="988", sms_chat="Ketik HOME ke 741741"),
            InfoHotline(kode_negara="us", nama_layanan="Emergency Medical Services", nomor="911"),
        ],
        "uk": [
            InfoHotline(kode_negara="uk", nama_layanan="NHS Mental Health Services", nomor="111"),
            InfoHotline(kode_negara="uk", nama_layanan="Samaritans UK", nomor="116 123"),
            InfoHotline(kode_negara="uk", nama_layanan="Emergency Services", nomor="999"),
        ],
        "au": [
            InfoHotline(kode_negara="au", nama_layanan="Lifeline Australia", nomor="13 11 14", sms_chat="SMS 0477 13 11 14"),
            InfoHotline(kode_negara="au", nama_layanan="Emergency", nomor="000"),
        ],
        "sg": [
            InfoHotline(kode_negara="sg", nama_layanan="Samaritans of Singapore (SOS)", nomor="1-767", sms_chat="WhatsApp 9151 1767"),
            InfoHotline(kode_negara="sg", nama_layanan="Emergency Ambulance", nomor="995"),
        ],
        "my": [
            InfoHotline(kode_negara="my", nama_layanan="Talian HEAL KKM (Kesihatan Mental)", nomor="15555"),
            InfoHotline(kode_negara="my", nama_layanan="Talian Kasih", nomor="15999", sms_chat="WhatsApp 019-2615999"),
            InfoHotline(kode_negara="my", nama_layanan="Kecemasan / Polis / Ambulans", nomor="999"),
        ],
        "gl": [
            InfoHotline(kode_negara="gl", nama_layanan="Befrienders Worldwide", nomor="Kunjungi www.befrienders.org", tersedia="Direktori Global"),
            InfoHotline(kode_negara="gl", nama_layanan="IASP Crisis Centres", nomor="Kunjungi www.iasp.info/resources/Crisis_Centres", tersedia="Direktori Global"),
        ],
    }

    @classmethod
    def dapatkan_hotline(cls, geo: str = "id") -> list[InfoHotline]:
        g = geo.lower().strip()
        return cls.HOTLINES.get(g, cls.HOTLINES["id"])


def format_rujukan_geo(geo: str = "id", nama_pengguna: str | None = None) -> str:
    """Menyusun kalimat rujukan krisis 4-komponen standar klinis Dr. Anna Reed."""
    daftar_kontak = DirektoriHotline.dapatkan_hotline(geo)
    baris_kontak = "\n".join([f"- {h.nama_layanan}: {h.nomor} ({h.tersedia})" for h in daftar_kontak])

    sapaan = f", {nama_pengguna}" if nama_pengguna else ""

    bagian_1 = f"Aku mendengar betapa berat dan melelahkannya apa yang sedang kamu hadapi saat ini{sapaan}."
    bagian_2 = (
        "Sebagai pendamping digital, kapasitas teknologi ini memiliki batas nyata "
        "dan aku tidak bisa menggantikan bantuan langsung manusia untuk menjamin keselamatanmu."
    )
    bagian_3 = (
        "Keselamatanmu adalah hal yang paling berharga. Tolong segera hubungi layanan profesional sekarang:\n"
        f"{baris_kontak}\n"
        "- IGD Rumah Sakit terdekat atau orang terpercaya di sekitarmu."
    )
    bagian_4 = (
        "Maukah kamu berjanji untuk tetap berada di tempat yang aman dan menghubungi nomor di atas saat ini juga? "
        "Aku tetap di sini menemanimu bernapas perlahan sampai bantuan tiba."
    )

    return f"{bagian_1}\n\n{bagian_2}\n\n{bagian_3}\n\n{bagian_4}"
