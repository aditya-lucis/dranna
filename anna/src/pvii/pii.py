# anna/src/pvii/pii.py — sanitasi & anonimisasi data pribadi sensitif (PII / UU PDP)
"""
Sanitizer Data Pribadi Sensitif (UU No. 27/2022 Pelindungan Data Pribadi & GDPR):
- NIK (Nomor Induk Kependudukan 16 digit)
- Nomor Telepon Indonesia (+62 / 08xx)
- Alamat Email
- Nomor Kartu Pembayaran / Rekening Bank
"""
import re


class SanitizerPII:
    """Modul deteksi dan redaksi data identitas pribadi (PII)."""

    POLA_NIK = r"\b[1-9]\d{15}\b"
    POLA_HP = r"\b(?:\+62|62|0)8[1-9][0-9]{7,10}\b"
    POLA_EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    POLA_KARTU = r"\b(?:\d{4}[ -]?){3}\d{4}\b"

    @classmethod
    def redaksi(cls, teks: str) -> tuple[str, list[str]]:
        """Meredaksi PII dari teks masukan dan mengembalikan teks bersih serta daftar entitas yang teredaksi."""
        entitas_ditemukan = []
        hasil = teks

        # 1. NIK
        if re.search(cls.POLA_NIK, hasil):
            entitas_ditemukan.append("NIK")
            hasil = re.sub(cls.POLA_NIK, "[TEREDAKSI-NIK]", hasil)

        # 2. Nomor Kartu
        if re.search(cls.POLA_KARTU, hasil):
            entitas_ditemukan.append("KARTU_KEUANGAN")
            hasil = re.sub(cls.POLA_KARTU, "[TEREDAKSI-KARTU]", hasil)

        # 3. Nomor Telepon
        if re.search(cls.POLA_HP, hasil):
            entitas_ditemukan.append("NOMOR_HP")
            hasil = re.sub(cls.POLA_HP, "[TEREDAKSI-HP]", hasil)

        # 4. Email
        if re.search(cls.POLA_EMAIL, hasil):
            entitas_ditemukan.append("EMAIL")
            hasil = re.sub(cls.POLA_EMAIL, "[TEREDAKSI-EMAIL]", hasil)

        return hasil, entitas_ditemukan


def redaksi_pii(teks: str) -> str:
    """Helper cepat untuk meredaksi PII dari string teks."""
    bersih, _ = SanitizerPII.redaksi(teks)
    return bersih
