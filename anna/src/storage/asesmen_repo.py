# anna/src/storage/asesmen_repo.py — repositori persistensi asesmen klinis PHQ-9 & GAD-7
import json
import uuid
import datetime
from pathlib import Path
from pydantic import BaseModel, Field

from anna.src.storage.db import get_connection, init_db
from anna.src.klinik.phq9 import skor_phq9
from anna.src.klinik.gad7 import skor_gad7
from anna.src.pvi.hotlines import DirektoriHotline, format_rujukan_geo


class AsesmenSubmit(BaseModel):
    jenis: str = Field(pattern="^(phq9|gad7)$")
    jawaban: list[int] = Field(min_length=7, max_length=9)
    geo: str = "id"


class AsesmenRecord(BaseModel):
    id: str
    user_id: str
    jenis_asesmen: str
    skor_total: int
    kategori: str
    item9_positif: bool
    jawaban_rinci: list[int]
    dibuat_pada: str
    kategori_adalah_diagnosis: bool = False
    krisis_darurat: bool = False
    pesan_rujukan: str | None = None
    hotlines: list[dict] | None = None


class AsesmenRepository:
    """Repository penyimpan hasil asesmen PHQ-9 dan GAD-7 dengan penegakan hard-gate."""

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path
        init_db(self.db_path)

    def proses_dan_simpan(self, user_id: str, data: AsesmenSubmit) -> AsesmenRecord:
        """Memproses skor asesmen, memeriksa killswitch item-9, dan menyimpan ke database."""
        cid = f"eval-{uuid.uuid4().hex[:12]}"
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if data.jenis == "phq9":
            res = skor_phq9(data.jawaban)
            skor_total = res["total"]
            kategori = res["kategori"]
            item9 = res["item9_menyakiti_diri"]
        else:
            res = skor_gad7(data.jawaban)
            skor_total = res["total"]
            kategori = res["kategori"]
            item9 = False

        pesan_rujuk = None
        daftar_kontak = None
        krisis = False

        # Hard-Gate Killswitch pada Item-9 PHQ-9
        if item9:
            krisis = True
            pesan_rujuk = format_rujukan_geo(geo=data.geo)
            raw_hotlines = DirektoriHotline.dapatkan_hotline(data.geo)
            daftar_kontak = [
                {"nama": h.nama_layanan, "nomor": h.nomor, "sms_chat": h.sms_chat or "", "tersedia": h.tersedia}
                for h in raw_hotlines
            ]

        # Simpan ke SQLite WAL
        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO asesmen_klinis (
                    id, user_id, jenis_asesmen, skor_total, kategori, 
                    item9_positif, jawaban_rinci, dibuat_pada
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cid,
                    user_id,
                    data.jenis,
                    skor_total,
                    kategori,
                    int(item9),
                    json.dumps(data.jawaban),
                    now_iso,
                ),
            )

        return AsesmenRecord(
            id=cid,
            user_id=user_id,
            jenis_asesmen=data.jenis,
            skor_total=skor_total,
            kategori=kategori,
            item9_positif=item9,
            jawaban_rinci=data.jawaban,
            dibuat_pada=now_iso,
            kategori_adalah_diagnosis=False,
            krisis_darurat=krisis,
            pesan_rujukan=pesan_rujuk,
            hotlines=daftar_kontak,
        )

    def ambil_riwayat(self, user_id: str, limit: int = 10) -> list[AsesmenRecord]:
        """Mengambil riwayat asesmen pengguna terurut dari yang terbaru."""
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                SELECT id, user_id, jenis_asesmen, skor_total, kategori, 
                       item9_positif, jawaban_rinci, dibuat_pada
                FROM asesmen_klinis
                WHERE user_id = ?
                ORDER BY dibuat_pada DESC
                LIMIT ?
                """,
                (user_id, limit),
            )
            rows = cur.fetchall()
            hasil = []
            for r in rows:
                hasil.append(
                    AsesmenRecord(
                        id=r["id"],
                        user_id=r["user_id"],
                        jenis_asesmen=r["jenis_asesmen"],
                        skor_total=r["skor_total"],
                        kategori=r["kategori"],
                        item9_positif=bool(r["item9_positif"]),
                        jawaban_rinci=json.loads(r["jawaban_rinci"]),
                        dibuat_pada=r["dibuat_pada"],
                        kategori_adalah_diagnosis=False,
                    )
                )
            return hasil

