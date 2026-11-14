# anna/src/storage/homework_repo.py — repository tugas mikro & Behavioral Activation (Fase 4)
"""
Homework & Behavioral Activation Repository (Fase 4):
- Menyimpan tugas mikro antar-sesi (latihan napas, thought record, tindakan komitmen nilai).
- Menjaga kontinuitas multi-sesi dengan pendekatan suportif tanpa menghakimi (guilt-free).
- Mematuhi prinsip Zero-PII dan Right to be Forgotten (RTBF).
"""
import uuid
from pathlib import Path
from pydantic import BaseModel, Field
from anna.src.storage.db import get_connection, init_db


class HomeworkItem(BaseModel):
    id: str = Field(default_factory=lambda: "hw-" + uuid.uuid4().hex[:8])
    user_id: str
    kategori: str  # "napas" | "thought_record" | "values" | "aktivitas_ba"
    deskripsi: str
    status: str = "pending"  # "pending" | "selesai" | "dilewati"
    tenggat_waktu: str | None = None
    refleksi_pengguna: str | None = None
    dibuat_pada: str | None = None
    diperbarui_pada: str | None = None


class HomeworkRepository:
    """Pengelola siklus hidup tugas rumah terapeutik antar-sesi."""

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path
        init_db(self.db_path)

    def tambah_tugas(
        self,
        user_id: str,
        kategori: str,
        deskripsi: str,
        tenggat_waktu: str | None = None,
    ) -> HomeworkItem:
        """Membuat tugas mikro baru untuk pengguna."""
        item = HomeworkItem(
            user_id=user_id,
            kategori=kategori,
            deskripsi=deskripsi,
            tenggat_waktu=tenggat_waktu,
        )
        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO homework_tasks (
                    id, user_id, kategori, deskripsi, status, tenggat_waktu
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (item.id, item.user_id, item.kategori, item.deskripsi, item.status, item.tenggat_waktu),
            )
        return item

    def ambil_tugas_pending(self, user_id: str, limit: int = 5) -> list[HomeworkItem]:
        """Mengambil tugas yang belum diselesaikan oleh pengguna."""
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                SELECT * FROM homework_tasks 
                WHERE user_id = ? AND status = 'pending'
                ORDER BY dibuat_pada ASC LIMIT ?
                """,
                (user_id, limit),
            )
            rows = cur.fetchall()
            return [
                HomeworkItem(
                    id=row["id"],
                    user_id=row["user_id"],
                    kategori=row["kategori"],
                    deskripsi=row["deskripsi"],
                    status=row["status"],
                    tenggat_waktu=row["tenggat_waktu"],
                    refleksi_pengguna=row["refleksi_pengguna"],
                    dibuat_pada=row["dibuat_pada"],
                    diperbarui_pada=row["diperbarui_pada"],
                )
                for row in rows
            ]

    def ambil_riwayat_tugas(self, user_id: str, limit: int = 20) -> list[HomeworkItem]:
        """Mengambil seluruh riwayat tugas pengguna (baik pending, selesai, maupun dilewati)."""
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                SELECT * FROM homework_tasks 
                WHERE user_id = ? 
                ORDER BY dibuat_pada DESC LIMIT ?
                """,
                (user_id, limit),
            )
            rows = cur.fetchall()
            return [
                HomeworkItem(
                    id=row["id"],
                    user_id=row["user_id"],
                    kategori=row["kategori"],
                    deskripsi=row["deskripsi"],
                    status=row["status"],
                    tenggat_waktu=row["tenggat_waktu"],
                    refleksi_pengguna=row["refleksi_pengguna"],
                    dibuat_pada=row["dibuat_pada"],
                    diperbarui_pada=row["diperbarui_pada"],
                )
                for row in rows
            ]

    def perbarui_status(
        self,
        task_id: str,
        user_id: str,
        status: str,
        refleksi: str | None = None,
    ) -> bool:
        """Memperbarui status tugas (selesai / dilewati) beserta catatan refleksi."""
        if status not in ("pending", "selesai", "dilewati"):
            status = "pending"

        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                UPDATE homework_tasks 
                SET status = ?, refleksi_pengguna = ?, diperbarui_pada = CURRENT_TIMESTAMP
                WHERE id = ? AND user_id = ?
                """,
                (status, refleksi, task_id, user_id),
            )
            return cur.rowcount > 0

    def bangun_ringkasan_homework_awal_sesi(self, user_id: str) -> str:
        """Menghasilkan teks pengingat hangat untuk prompt pembuka sesi tanpa menghakimi."""
        pending = self.ambil_tugas_pending(user_id, limit=2)
        if not pending:
            return ""

        daftar = "; ".join(f"[{p.kategori}] {p.deskripsi}" for p in pending)
        return (
            f"TUGAS MIKRO MANDIRI PENGGUNA YANG SEDANG AKTIF: {daftar}. "
            "INSTRUKSI: Tanyakan kabar terkait hal ini dengan sangat lembut, hangat, dan tanpa menghakimi. "
            "Jika pengguna belum sempat melakukannya, katakan bahwa hal itu sangat manusiawi dan tidak apa-apa."
        )

