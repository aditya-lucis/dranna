# anna/src/pvii/consent.py — consent-first protocol & batasan privasi sesi pengguna
"""
Consent-First Protocol (Bab 104):
- Meminta konfirmasi eksplisit pengguna sebelum eksplorasi mendalam topik sensitif
- Menyediakan hak penghapusan data / lupakan sesi (Right to be Forgotten)
- Melacak status persetujuan per sesi secara transparan
"""
from pydantic import BaseModel


class StatusPersetujuan(BaseModel):
    sesi_id: str
    izin_psikoedukasi_mendalam: bool = False
    izin_simpan_riwayat: bool = True
    topik_sensitif_diizinkan: list[str] = []


class ManajerConsent:
    """Pengelola status persetujuan dan kendali privasi pengguna."""

    def __init__(self):
        self._consent_store: dict[str, StatusPersetujuan] = {}

    def dapatkan_status(self, sesi_id: str) -> StatusPersetujuan:
        if sesi_id not in self._consent_store:
            self._consent_store[sesi_id] = StatusPersetujuan(sesi_id=sesi_id)
        return self._consent_store[sesi_id]

    def beri_izin_topik(self, sesi_id: str, topik: str):
        st = self.dapatkan_status(sesi_id)
        if topik not in st.topik_sensitif_diizinkan:
            st.topik_sensitif_diizinkan.append(topik)

    def cabut_izin_riwayat(self, sesi_id: str):
        st = self.dapatkan_status(sesi_id)
        st.izin_simpan_riwayat = False

    def hapus_sesi_total(self, sesi_id: str) -> bool:
        if sesi_id in self._consent_store:
            del self._consent_store[sesi_id]
            return True
        return False
