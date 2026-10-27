# anna/src/pvii/audit.py — audit trail kriptografis & logging privasi terdesentralisasi
"""
Audit Trail Kriptografis (Bab 106 & Kepatuhan UU PDP):
- Mencatat jejak audit peristiwa klinis & etika dengan hashing SHA-256
- Zero-PII storage: Hanya menyimpan hash anonim dari pesan, bukan data pribadi mentah
- Memungkinkan pembuktian integritas tanpa melanggar kerahasiaan pasien
"""
import hashlib
import time
from pydantic import BaseModel


class CatatanAudit(BaseModel):
    waktu: float
    sesi_id: str
    jenis_peristiwa: str  # "krisis" | "jailbreak" | "pii_diredaksi" | "medis_gate"
    hash_pesan: str
    level_peringatan: str


class LoggerAuditPrivasi:
    """Pencatat audit kepatuhan etika & privasi."""

    def __init__(self):
        self._log: list[CatatanAudit] = []

    @staticmethod
    def hitung_hash(teks: str) -> str:
        """Menghitung ringkasan kriptografis SHA-256 dari teks."""
        return hashlib.sha256(teks.encode("utf-8")).hexdigest()

    def catat(self, sesi_id: str, jenis_peristiwa: str, teks_pesan: str, level: str = "INFO"):
        h = self.hitung_hash(teks_pesan)
        catatan = CatatanAudit(
            waktu=time.time(),
            sesi_id=sesi_id,
            jenis_peristiwa=jenis_peristiwa,
            hash_pesan=h,
            level_peringatan=level,
        )
        self._log.append(catatan)
        return catatan

    def riwayat_sesi(self, sesi_id: str) -> list[CatatanAudit]:
        return [c for c in self._log if c.sesi_id == sesi_id]

    def total_catatan(self) -> int:
        return len(self._log)
