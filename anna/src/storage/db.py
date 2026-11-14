# anna/src/storage/db.py — koneksi & inisialisasi SQLite WAL untuk persistensi data Dr. Anna Reed
"""
Lapisan database lokal berkinerja tinggi menggunakan SQLite WAL (Write-Ahead Logging):
- Sangat ringan, zero-setup, aman untuk concurency multi-read & single-write
- Schema terstruktur untuk: Consent, Jurnal Mood, Safety Plan, Memori Episodik, dan Asesmen
- Menghormati prinsip Zero-PII dan Right to be Forgotten
"""
import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

# Default database path di folder data/
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
DEFAULT_DB_PATH = DATA_DIR / "anna_reed.db"


def get_db_path() -> Path:
    db_env = os.environ.get("ANNA_DB_PATH")
    if db_env:
        return Path(db_env)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_DB_PATH


@contextmanager
def get_connection(db_path: Path | None = None):
    """Context manager untuk koneksi SQLite dengan konfigurasi WAL mode & foreign keys."""
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=15.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path: Path | None = None):
    """Menginisialisasi tabel-tabel utama Project Serenity Fase 2."""
    with get_connection(db_path) as conn:
        conn.executescript("""
        -- 1. Consent Ledger (Persetujuan 5-komponen)
        CREATE TABLE IF NOT EXISTS consent_ledger (
            user_id TEXT PRIMARY KEY,
            izin_psikoedukasi INTEGER DEFAULT 1,
            izin_simpan_riwayat INTEGER DEFAULT 1,
            izin_analisis_mood INTEGER DEFAULT 1,
            izin_analisis_ekspresi INTEGER DEFAULT 0,
            durasi_simpan_hari INTEGER DEFAULT 90,
            topik_sensitif_diizinkan TEXT DEFAULT '[]',
            dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            diperbarui_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 2. Mood Logs (Catatan valence & energi harian)
        CREATE TABLE IF NOT EXISTS mood_logs (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            waktu_iso TEXT NOT NULL,
            mood_skor REAL NOT NULL,
            energi_skor REAL NOT NULL,
            catatan_refleksi TEXT,
            hal_yang_disyukuri TEXT DEFAULT '[]',
            dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_mood_user_waktu ON mood_logs(user_id, waktu_iso);

        -- 3. Safety Plans (Stanley-Brown Model)
        CREATE TABLE IF NOT EXISTS safety_plans (
            user_id TEXT PRIMARY KEY,
            tanda_peringatan TEXT NOT NULL,      -- JSON array
            strategi_koping TEXT NOT NULL,       -- JSON array
            kontak_personal TEXT NOT NULL,       -- JSON array
            kontak_profesional TEXT NOT NULL,    -- JSON array
            langkungan_aman TEXT NOT NULL,       -- JSON array
            diperbarui_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 4. Episodic Memories (Ringkasan sesi ter-sanitasi Zero-PII)
        CREATE TABLE IF NOT EXISTS episodic_memories (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            sesi_id TEXT NOT NULL,
            waktu_iso TEXT NOT NULL,
            topik TEXT NOT NULL,
            ringkasan_konteks TEXT NOT NULL,
            valence_rata_rata REAL DEFAULT 0.0,
            teknik_efektif TEXT,
            dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_memori_user ON episodic_memories(user_id);

        -- 5. Asesmen Klinis (PHQ-9 / GAD-7 skor non-diagnostik)
        CREATE TABLE IF NOT EXISTS asesmen_klinis (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            jenis_asesmen TEXT NOT NULL,         -- 'phq9' | 'gad7'
            skor_total INTEGER NOT NULL,
            kategori TEXT NOT NULL,              -- 'minimal' | 'ringan' | 'sedang' | dll
            item9_positif INTEGER DEFAULT 0,
            jawaban_rinci TEXT NOT NULL,         -- JSON array
            dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_asesmen_user ON asesmen_klinis(user_id);

        -- 6. Homework Antar-Sesi & Behavioral Activation (Fase 4)
        CREATE TABLE IF NOT EXISTS homework_tasks (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            kategori TEXT NOT NULL,              -- 'napas' | 'thought_record' | 'values' | 'aktivitas_ba'
            deskripsi TEXT NOT NULL,
            status TEXT DEFAULT 'pending',       -- 'pending' | 'selesai' | 'dilewati'
            tenggat_waktu TEXT,                  -- ISO timestamp
            refleksi_pengguna TEXT,
            dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            diperbarui_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_homework_user_status ON homework_tasks(user_id, status);

        -- 7. Audit Event Logs (Zero-PII Compliance & Safety Tracking - Fase 5)
        CREATE TABLE IF NOT EXISTS audit_event_logs (
            id TEXT PRIMARY KEY,
            tipe_peristiwa TEXT NOT NULL,        -- 'eskalasi_krisis' | 'rtbf_dihapus' | 'ekspor_data' | 'audit_rilis'
            eskalasi TEXT DEFAULT 'GREEN',
            metadata_json TEXT DEFAULT '{}',
            waktu_iso TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_audit_waktu ON audit_event_logs(waktu_iso);
        """)
        try:
            conn.execute("ALTER TABLE consent_ledger ADD COLUMN izin_analisis_ekspresi INTEGER DEFAULT 0;")
        except sqlite3.OperationalError:
            pass  # Kolom sudah ada


