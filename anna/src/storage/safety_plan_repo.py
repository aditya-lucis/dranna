# anna/src/storage/safety_plan_repo.py — repository rencana keselamatan Stanley-Brown model
import json
import datetime
from pathlib import Path
from pydantic import BaseModel, Field
from anna.src.storage.db import get_connection, init_db
from anna.src.pvi.hotlines import DirektoriHotline


class KontakItem(BaseModel):
    nama: str
    kontak_info: str
    keterangan: str = ""


class SafetyPlanModel(BaseModel):
    user_id: str
    tanda_peringatan: list[str] = Field(default_factory=list)
    strategi_koping: list[str] = Field(default_factory=list)
    kontak_personal: list[KontakItem] = Field(default_factory=list)
    kontak_profesional: list[KontakItem] = Field(default_factory=list)
    lingkungan_aman: list[str] = Field(default_factory=list)
    diperbarui_pada: str = ""


class SafetyPlanRepository:
    """Pengelola penyimpanan dan pemuatan rencana keselamatan (Safety Plan) pribadi pengguna."""

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path
        init_db(self.db_path)

    def default_plan(self, user_id: str, geo: str = "id") -> SafetyPlanModel:
        """Membuat draf rencana keselamatan awal dengan hotline resmi terisi otomatis."""
        raw_hotlines = DirektoriHotline.dapatkan_hotline(geo)
        kontak_prof = [
            KontakItem(nama=h.nama_layanan, kontak_info=h.nomor, keterangan=h.tersedia)
            for h in raw_hotlines
        ]
        kontak_prof.append(
            KontakItem(nama="IGD Rumah Sakit Terdekat", kontak_info="112 / 119", keterangan="Layanan Darurat Medis")
        )

        return SafetyPlanModel(
            user_id=user_id,
            tanda_peringatan=[
                "Mulai menarik diri dari percakapan teman atau keluarga",
                "Pikiran berulang bahwa beban ini tidak ada ujungnya",
                "Pola tidur berantakan (tidak tidur atau tidur seharian)",
            ],
            strategi_koping=[
                "Melatih pernapasan ritmis 4-7-8 selama 5 siklus",
                "Mencuci wajah atau tangan dengan air dingin (TIPP - T)",
                "Mendengarkan playlist musik yang menenangkan",
            ],
            kontak_personal=[
                KontakItem(nama="Sahabat Terpercaya", kontak_info="[Isi nomor/kontak]", keterangan="Bisa ditelepon kapan pun"),
                KontakItem(nama="Keluarga Dekat", kontak_info="[Isi kontak keluarga]", keterangan="Dukungan rumah"),
            ],
            kontak_profesional=kontak_prof,
            lingkungan_aman=[
                "Menjauhkan benda-benda tajam atau obat berlebih ke tempat aman",
                "Memastikan pintu kamar tidak terkunci dan ada orang terdekat",
            ],
            diperbarui_pada=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )

    def ambil_safety_plan(self, user_id: str, geo: str = "id") -> SafetyPlanModel:
        """Mengambil Safety Plan pengguna atau menghasilkan template default bila belum ada."""
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                SELECT tanda_peringatan, strategi_koping, kontak_personal, 
                       kontak_profesional, langkungan_aman, diperbarui_pada
                FROM safety_plans
                WHERE user_id = ?
                """,
                (user_id,),
            )
            row = cur.fetchone()
            if not row:
                return self.default_plan(user_id, geo=geo)

            return SafetyPlanModel(
                user_id=user_id,
                tanda_peringatan=json.loads(row["tanda_peringatan"] or "[]"),
                strategi_koping=json.loads(row["strategi_koping"] or "[]"),
                kontak_personal=[KontakItem(**k) for k in json.loads(row["kontak_personal"] or "[]")],
                kontak_profesional=[KontakItem(**k) for k in json.loads(row["kontak_profesional"] or "[]")],
                lingkungan_aman=json.loads(row["langkungan_aman"] or "[]"),
                diperbarui_pada=row["diperbarui_pada"] or "",
            )

    def simpan_safety_plan(self, plan: SafetyPlanModel) -> SafetyPlanModel:
        """Menyimpan atau memperbarui Safety Plan pengguna ke SQLite WAL."""
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        plan.diperbarui_pada = now_iso

        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO safety_plans (
                    user_id, tanda_peringatan, strategi_koping, kontak_personal,
                    kontak_profesional, langkungan_aman, diperbarui_pada
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    tanda_peringatan = excluded.tanda_peringatan,
                    strategi_koping = excluded.strategi_koping,
                    kontak_personal = excluded.kontak_personal,
                    kontak_profesional = excluded.kontak_profesional,
                    langkungan_aman = excluded.langkungan_aman,
                    diperbarui_pada = excluded.diperbarui_pada
                """,
                (
                    plan.user_id,
                    json.dumps(plan.tanda_peringatan),
                    json.dumps(plan.strategi_koping),
                    json.dumps([k.model_dump() for k in plan.kontak_personal]),
                    json.dumps([k.model_dump() for k in plan.kontak_profesional]),
                    json.dumps(plan.lingkungan_aman),
                    now_iso,
                ),
            )
        return plan

