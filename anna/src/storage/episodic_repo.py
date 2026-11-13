# anna/src/storage/episodic_repo.py — memori episodik jangka panjang dengan jaminan Zero-PII
import uuid
import datetime
from pathlib import Path
from pydantic import BaseModel, Field

from anna.src.storage.db import get_connection, init_db
from anna.src.pvii.pii import redaksi_pii


class MemoriEpisodik(BaseModel):
    id: str
    user_id: str
    sesi_id: str
    waktu_iso: str
    topik: str
    ringkasan_konteks: str
    valence_rata_rata: float = 0.0
    teknik_efektif: str | None = None


class EpisodicRepository:
    """Pengelola penyimpanan dan pemanggilan memori episodik jangka panjang yang aman dari PII."""

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path
        init_db(self.db_path)

    def simpan_memori(
        self,
        user_id: str,
        sesi_id: str,
        topik: str,
        ringkasan: str,
        valence: float = 0.0,
        teknik: str | None = None,
    ) -> MemoriEpisodik:
        """Menyimpan ringkasan sesi ke basis data setelah disanitasi Zero-PII."""
        cid = f"ep-{uuid.uuid4().hex[:12]}"
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        ringkasan_bersih = redaksi_pii(ringkasan)

        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO episodic_memories (
                    id, user_id, sesi_id, waktu_iso, topik,
                    ringkasan_konteks, valence_rata_rata, teknik_efektif
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cid,
                    user_id,
                    sesi_id,
                    now_iso,
                    topik,
                    ringkasan_bersih,
                    float(valence),
                    teknik,
                ),
            )

        return MemoriEpisodik(
            id=cid,
            user_id=user_id,
            sesi_id=sesi_id,
            waktu_iso=now_iso,
            topik=topik,
            ringkasan_konteks=ringkasan_bersih,
            valence_rata_rata=valence,
            teknik_efektif=teknik,
        )

    def ambil_memori_terbaru(self, user_id: str, limit: int = 3) -> list[MemoriEpisodik]:
        """Mengambil rekaman memori episodik terbaru pengguna."""
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                SELECT id, user_id, sesi_id, waktu_iso, topik,
                       ringkasan_konteks, valence_rata_rata, teknik_efektif
                FROM episodic_memories
                WHERE user_id = ?
                ORDER BY waktu_iso DESC
                LIMIT ?
                """,
                (user_id, limit),
            )
            rows = cur.fetchall()
            hasil = []
            for r in rows:
                hasil.append(
                    MemoriEpisodik(
                        id=r["id"],
                        user_id=r["user_id"],
                        sesi_id=r["sesi_id"],
                        waktu_iso=r["waktu_iso"],
                        topik=r["topik"],
                        ringkasan_konteks=r["ringkasan_konteks"],
                        valence_rata_rata=float(r["valence_rata_rata"]),
                        teknik_efektif=r["teknik_efektif"],
                    )
                )
            return hasil

    def bangun_konteks_ringkasan(self, user_id: str, limit: int = 2) -> str:
        """Menyusun benang merah ringkasan sesi lampau untuk diinjeksikan ke prompt Anna."""
        terbaru = self.ambil_memori_terbaru(user_id, limit=limit)
        if not terbaru:
            return ""

        poin = []
        for m in reversed(terbaru):
            poin.append(f"Topik {m.topik}: {m.ringkasan_konteks[:100]}")
        return " | ".join(poin)

