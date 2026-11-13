# anna/src/storage/mood_repo.py — repository persistensi mood log & deteksi flatline 7 hari
import json
import uuid
import datetime
from pathlib import Path
from pydantic import BaseModel, Field
import numpy as np

from anna.src.storage.db import get_connection, init_db
from anna.src.pix.journal import CatatanJurnal


class AnalisisMood(BaseModel):
    total_entri: int
    rata_rata_mood: float
    rata_rata_energi: float
    tren: str  # "stabil" | "meningkat" | "menurun" | "fluktuatif"
    flatline_terdeteksi: bool
    pesan_evaluasi: str
    rekomendasi_rujukan: bool


class MoodRepository:
    """Repository database SQLite WAL untuk pencatatan mood & deteksi flatline emosi."""

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path
        init_db(self.db_path)

    def simpan_catatan(self, user_id: str, catatan: CatatanJurnal) -> CatatanJurnal:
        """Menyimpan entri catatan mood harian pengguna ke basis data SQLite WAL."""
        waktu = catatan.waktu_iso or datetime.datetime.now(datetime.timezone.utc).isoformat()
        cid = catatan.id or f"mood-{uuid.uuid4().hex[:12]}"
        catatan.id = cid
        catatan.waktu_iso = waktu

        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO mood_logs (
                    id, user_id, waktu_iso, mood_skor, energi_skor, 
                    catatan_refleksi, hal_yang_disyukuri
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    mood_skor = excluded.mood_skor,
                    energi_skor = excluded.energi_skor,
                    catatan_refleksi = excluded.catatan_refleksi,
                    hal_yang_disyukuri = excluded.hal_yang_disyukuri,
                    waktu_iso = excluded.waktu_iso
                """,
                (
                    cid,
                    user_id,
                    waktu,
                    float(catatan.mood_skor),
                    float(catatan.energi_skor),
                    catatan.catatan_refleksi,
                    json.dumps(catatan.hal_yang_disyukuri),
                ),
            )
        return catatan

    def ambil_riwayat(self, user_id: str, limit: int = 14) -> list[CatatanJurnal]:
        """Mengambil riwayat entri catatan mood terkini pengguna."""
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                SELECT id, waktu_iso, mood_skor, energi_skor, catatan_refleksi, hal_yang_disyukuri
                FROM mood_logs
                WHERE user_id = ?
                ORDER BY waktu_iso ASC
                LIMIT ?
                """,
                (user_id, limit),
            )
            rows = cur.fetchall()
            hasil = []
            for r in rows:
                hasil.append(
                    CatatanJurnal(
                        id=r["id"],
                        waktu_iso=r["waktu_iso"],
                        mood_skor=float(r["mood_skor"]),
                        energi_skor=float(r["energi_skor"]),
                        catatan_refleksi=r["catatan_refleksi"] or "",
                        hal_yang_disyukuri=json.loads(r["hal_yang_disyukuri"] or "[]"),
                    )
                )
            return hasil

    def analisis_flatline(self, user_id: str, ambang_hari: int = 7) -> AnalisisMood:
        """Menganalisis tren mood 7-14 entri terakhir untuk mendeteksi Kondisi Wajib Berhenti #4 (Flatline >= 7 hari)."""
        riwayat = self.ambil_riwayat(user_id, limit=max(ambang_hari, 14))
        if not riwayat:
            return AnalisisMood(
                total_entri=0,
                rata_rata_mood=0.0,
                rata_rata_energi=0.0,
                tren="stabil",
                flatline_terdeteksi=False,
                pesan_evaluasi="Belum ada catatan jurnal yang tersimpan.",
                rekomendasi_rujukan=False,
            )

        moods = np.array([c.mood_skor for c in riwayat], dtype=float)
        energies = np.array([c.energi_skor for c in riwayat], dtype=float)

        rata_mood = round(float(np.mean(moods)), 2)
        rata_energi = round(float(np.mean(energies)), 2)

        # Evaluasi tren jika entri >= 3
        if len(moods) >= 3:
            kemiringan = float(moods[-1] - moods[0])
            if kemiringan > 0.25:
                tren = "meningkat"
            elif kemiringan < -0.25:
                tren = "menurun"
            elif np.std(moods) > 0.35:
                tren = "fluktuatif"
            else:
                tren = "stabil"
        else:
            tren = "stabil"

        # Deteksi Flatline Mood >= 7 entri berturut-turut pada spektrum distres berat (mood <= -0.5)
        flatline = False
        if len(moods) >= ambang_hari:
            tujuh_terakhir = moods[-ambang_hari:]
            semua_berat = bool(np.all(tujuh_terakhir <= -0.5))
            std_rendah = bool(np.std(tujuh_terakhir) <= 0.25)  # Datar tanpa pemulihan
            if semua_berat and std_rendah:
                flatline = True

        if flatline:
            pesan = (
                f"Terdeteksi suasana hati berat yang datar selama {ambang_hari} hari berturut-turut. "
                "Sebagai pendamping AI, kapasitas teknologi ini terbatas dan ini adalah saat yang tepat "
                "untuk berkonsultasi langsung dengan psikolog klinis atau psikiater."
            )
            rekomendasi = True
        elif rata_mood < -0.3:
            pesan = "Suasana hatimu belakangan ini terasa cukup berat. Jangan ragu beristirahat dan melatih napas ritmis."
            rekomendasi = False
        else:
            pesan = "Pola suasana hatimu berada dalam rentang fluktuasi yang wajar dan adaptif."
            rekomendasi = False

        return AnalisisMood(
            total_entri=len(riwayat),
            rata_rata_mood=rata_mood,
            rata_rata_energi=rata_energi,
            tren=tren,
            flatline_terdeteksi=flatline,
            pesan_evaluasi=pesan,
            rekomendasi_rujukan=rekomendasi,
        )
