# anna/src/storage/export_service.py — ekspor portabilitas data UU PDP & pembersihan berkala TTL
"""
Layanan Portabilitas Data & Auto-TTL Pruning (Fase 5):
- Memenuhi mandat UU No. 27/2022 (UU PDP) & GDPR mengenai hak portabilitas data.
- Mengemas seluruh riwayat persetujuan, jurnal, safety plan, memori, asesmen, dan tugas
  ke dalam arsip JSON portabel yang bersih dan dapat dibaca manusia.
- Menyediakan fungsi pembersihan otomatis (TTL pruning) berdasarkan `durasi_simpan_hari`
  yang telah disetujui pengguna di Consent Ledger.
"""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json
import uuid

from anna.src.storage.db import get_connection, init_db
from anna.src.storage.consent_repo import ConsentRepository
from anna.src.storage.mood_repo import MoodRepository
from anna.src.storage.safety_plan_repo import SafetyPlanRepository
from anna.src.storage.episodic_repo import EpisodicRepository
from anna.src.storage.asesmen_repo import AsesmenRepository
from anna.src.storage.homework_repo import HomeworkRepository


def catat_audit_log(
    tipe_peristiwa: str,
    eskalasi: str = "GREEN",
    metadata: dict | None = None,
    db_path: Path | None = None,
):
    """Mencatat peristiwa audit kepatuhan tanpa PII ke dalam basis data."""
    now_iso = datetime.now(timezone.utc).isoformat()
    meta_json = json.dumps(metadata or {})
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO audit_event_logs (id, tipe_peristiwa, eskalasi, metadata_json, waktu_iso)
            VALUES (?, ?, ?, ?, ?)
            """,
            (f"aud-{uuid.uuid4().hex[:8]}", tipe_peristiwa, eskalasi, meta_json, now_iso),
        )


class ExportService:
    """Pengelola portabilitas data lengkap dan pembersihan berkala (Auto-TTL)."""

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path
        init_db(self.db_path)
        self.consent_repo = ConsentRepository(db_path)
        self.mood_repo = MoodRepository(db_path)
        self.safety_repo = SafetyPlanRepository(db_path)
        self.episodic_repo = EpisodicRepository(db_path)
        self.asesmen_repo = AsesmenRepository(db_path)
        self.homework_repo = HomeworkRepository(db_path)

    def ekspor_data_pengguna(self, user_id: str) -> dict:
        """Mengumpulkan seluruh data pengguna ke dalam satu paket JSON portabilitas."""
        c = self.consent_repo.dapatkan_consent(user_id)
        moods = self.mood_repo.ambil_riwayat(user_id, limit=500)
        sp = self.safety_repo.ambil_safety_plan(user_id)
        memories = self.episodic_repo.ambil_memori_terbaru(user_id, limit=200)
        asesmen = self.asesmen_repo.ambil_riwayat(user_id, limit=100)
        tasks = self.homework_repo.ambil_riwayat_tugas(user_id, limit=100)

        now_iso = datetime.now(timezone.utc).isoformat()
        paket_ekspor = {
            "standar_kepatuhan": "UU PDP No. 27/2022 & GDPR Article 20",
            "aplikasi": "Dr. Anna Reed (Project Serenity)",
            "user_id": user_id,
            "diekspor_pada": now_iso,
            "persetujuan_privasi": c.model_dump(),
            "rencana_keselamatan": sp.model_dump(),
            "catatan_mood_jurnal": [m.model_dump() for m in moods],
            "memori_episodik": [m.model_dump() for m in memories],
            "riwayat_asesmen_klinis": [a.model_dump() for a in asesmen],
            "tugas_mandiri_homework": [t.model_dump() for t in tasks],
            "total_entri": len(moods) + len(memories) + len(asesmen) + len(tasks),
        }

        # Catat peristiwa ekspor di audit log
        catat_audit_log(
            tipe_peristiwa="ekspor_data",
            eskalasi="GREEN",
            metadata={"user_id": user_id, "total_entri": paket_ekspor["total_entri"]},
            db_path=self.db_path,
        )

        return paket_ekspor

    def bersihkan_data_kedaluwarsa(
        self,
        user_id: str | None = None,
        durasi_hari_override: int | None = None,
    ) -> dict[str, int]:
        """Menghapus entri yang telah melampaui batas retensi `durasi_simpan_hari`."""
        laporan = {"mood_logs": 0, "episodic_memories": 0, "asesmen_klinis": 0, "homework_tasks": 0}

        # Dapatkan daftar user yang akan diproses
        with get_connection(self.db_path) as conn:
            if user_id:
                cur = conn.execute("SELECT user_id, durasi_simpan_hari FROM consent_ledger WHERE user_id = ?", (user_id,))
                user_list = [dict(row) for row in cur.fetchall()]
                if not user_list:
                    # Fallback jika user belum pernah membuka/menyimpan konfigurasi consent
                    user_list = [{"user_id": user_id, "durasi_simpan_hari": durasi_hari_override or 90}]
            else:
                cur = conn.execute("SELECT user_id, durasi_simpan_hari FROM consent_ledger")
                user_list = [dict(row) for row in cur.fetchall()]

            for u in user_list:
                uid = u["user_id"]
                hari = durasi_hari_override or u.get("durasi_simpan_hari") or 90
                batas_waktu = (datetime.now(timezone.utc) - timedelta(days=hari)).isoformat()

                # 1. Prune mood_logs
                c1 = conn.execute(
                    "DELETE FROM mood_logs WHERE user_id = ? AND waktu_iso < ?",
                    (uid, batas_waktu),
                )
                laporan["mood_logs"] += c1.rowcount

                # 2. Prune episodic_memories
                c2 = conn.execute(
                    "DELETE FROM episodic_memories WHERE user_id = ? AND dibuat_pada < ?",
                    (uid, batas_waktu),
                )
                laporan["episodic_memories"] += c2.rowcount

                # 3. Prune asesmen_klinis
                c3 = conn.execute(
                    "DELETE FROM asesmen_klinis WHERE user_id = ? AND dibuat_pada < ?",
                    (uid, batas_waktu),
                )
                laporan["asesmen_klinis"] += c3.rowcount

                # 4. Prune homework_tasks
                c4 = conn.execute(
                    "DELETE FROM homework_tasks WHERE user_id = ? AND dibuat_pada < ?",
                    (uid, batas_waktu),
                )
                laporan["homework_tasks"] += c4.rowcount

        total_dihapus = sum(laporan.values())
        if total_dihapus > 0:
            catat_audit_log(
                tipe_peristiwa="ttl_pruning_otomatis",
                eskalasi="GREEN",
                metadata={"total_dihapus": total_dihapus, "laporan": laporan},
                db_path=self.db_path,
            )

        return laporan

