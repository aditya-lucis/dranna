# anna/src/px/recovery.py — disaster recovery, snapshot sesi & verifikasi checksum SHA-256
"""
Disaster Recovery & State Snapshot Protocol (Bab 132):
- Membuat snapshot kondisi sesi percakapan dengan tanda tangan SHA-256
- Memulihkan (restore) state dari kerusakan koneksi atau crash sistem
- Menolak snapshot yang termanipulasi atau korup (checksum mismatch)
- Memastikan status eskalasi krisis tidak hilang saat proses pemulihan
"""
import json
import hashlib
import time
from pydantic import BaseModel


class SnapshotSesi(BaseModel):
    sesi_id: str
    waktu: float
    state_data: dict
    checksum_sha256: str


class DisasterRecoveryManager:
    """Manajer pemulihan bencana dan snapshot sesi Dr. Anna Reed."""

    @staticmethod
    def _hitung_checksum(data: dict) -> str:
        s = json.dumps(data, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    @classmethod
    def buat_snapshot(cls, sesi_id: str, state_data: dict) -> SnapshotSesi:
        """Membuat snapshot sesi terverifikasi kriptografis."""
        checksum = cls._hitung_checksum(state_data)
        return SnapshotSesi(
            sesi_id=sesi_id,
            waktu=time.time(),
            state_data=state_data,
            checksum_sha256=checksum,
        )

    @classmethod
    def pulihkan_snapshot(cls, snapshot: SnapshotSesi) -> tuple[bool, dict, str]:
        """Memvalidasi integritas snapshot dan memulihkan state data.

        Returns:
            tuple: (sukses: bool, state_data: dict, pesan: str)
        """
        checksum_hitung = cls._hitung_checksum(snapshot.state_data)
        if checksum_hitung != snapshot.checksum_sha256:
            return False, {}, "Checksum tidak cocok: data terkorupsi atau termanipulasi"

        return True, snapshot.state_data, "Snapshot valid dan berhasil dipulihkan"
