# anna/src/storage/consent_repo.py — repository consent ledger 5-komponen & right to be forgotten
import json
from pathlib import Path
from pydantic import BaseModel, Field
from anna.src.storage.db import get_connection, init_db


class ConsentData(BaseModel):
    user_id: str
    izin_psikoedukasi: bool = True
    izin_simpan_riwayat: bool = True
    izin_analisis_mood: bool = True
    durasi_simpan_hari: int = Field(default=90, ge=1, le=365)
    topik_sensitif_diizinkan: list[str] = Field(default_factory=list)


class ConsentRepository:
    """Pengelola hak data pengguna, persetujuan 5-komponen, dan penghapusan total (RTBF)."""

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path
        init_db(self.db_path)

    def dapatkan_consent(self, user_id: str) -> ConsentData:
        """Mengambil data persetujuan pengguna; mengembalikan default jika belum tercatat."""
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                "SELECT * FROM consent_ledger WHERE user_id = ?",
                (user_id,),
            )
            row = cur.fetchone()
            if not row:
                return ConsentData(user_id=user_id)

            return ConsentData(
                user_id=row["user_id"],
                izin_psikoedukasi=bool(row["izin_psikoedukasi"]),
                izin_simpan_riwayat=bool(row["izin_simpan_riwayat"]),
                izin_analisis_mood=bool(row["izin_analisis_mood"]),
                durasi_simpan_hari=row["durasi_simpan_hari"],
                topik_sensitif_diizinkan=json.loads(row["topik_sensitif_diizinkan"] or "[]"),
            )

    def simpan_consent(self, data: ConsentData) -> ConsentData:
        """Menyimpan atau memperbarui persetujuan pengguna."""
        topik_json = json.dumps(data.topik_sensitif_diizinkan)
        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO consent_ledger (
                    user_id, izin_psikoedukasi, izin_simpan_riwayat, 
                    izin_analisis_mood, durasi_simpan_hari, topik_sensitif_diizinkan,
                    diperbarui_pada
                ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    izin_psikoedukasi = excluded.izin_psikoedukasi,
                    izin_simpan_riwayat = excluded.izin_simpan_riwayat,
                    izin_analisis_mood = excluded.izin_analisis_mood,
                    durasi_simpan_hari = excluded.durasi_simpan_hari,
                    topik_sensitif_diizinkan = excluded.topik_sensitif_diizinkan,
                    diperbarui_pada = CURRENT_TIMESTAMP
                """,
                (
                    data.user_id,
                    int(data.izin_psikoedukasi),
                    int(data.izin_simpan_riwayat),
                    int(data.izin_analisis_mood),
                    data.durasi_simpan_hari,
                    topik_json,
                ),
            )
        return data

    def hapus_seluruh_data_user(self, user_id: str) -> dict[str, int]:
        """Right to be Forgotten (RTBF): Menghapus seluruh riwayat pengguna dari semua tabel database."""
        laporan = {}
        with get_connection(self.db_path) as conn:
            tabel_list = [
                ("mood_logs", "user_id"),
                ("safety_plans", "user_id"),
                ("episodic_memories", "user_id"),
                ("asesmen_klinis", "user_id"),
                ("consent_ledger", "user_id"),
            ]
            for tabel, col in tabel_list:
                cur = conn.execute(f"DELETE FROM {tabel} WHERE {col} = ?", (user_id,))
                laporan[tabel] = cur.rowcount
        return laporan

