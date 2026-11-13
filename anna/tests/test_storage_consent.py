# anna/tests/test_storage_consent.py — pengujian unit database SQLite WAL & consent repository
import os
import tempfile
from pathlib import Path
import pytest
from anna.src.storage.db import get_connection, init_db
from anna.src.storage.consent_repo import ConsentRepository, ConsentData


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        path = Path(f.name)
    init_db(path)
    yield path
    try:
        os.remove(path)
    except Exception:
        pass


def test_sqlite_wal_init(temp_db):
    """Memastikan SQLite berhasil diinisialisasi dalam WAL mode dan tabel terbuat."""
    with get_connection(temp_db) as conn:
        res = conn.execute("PRAGMA journal_mode;").fetchone()
        assert res[0].lower() == "wal"

        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()
        table_names = [t["name"] for t in tables]
        assert "consent_ledger" in table_names
        assert "mood_logs" in table_names
        assert "safety_plans" in table_names
        assert "episodic_memories" in table_names
        assert "asesmen_klinis" in table_names


def test_consent_repo_crud_dan_rtbf(temp_db):
    """Menguji penyimpanan consent 5-komponen dan penghapusan total (Right to be Forgotten)."""
    repo = ConsentRepository(db_path=temp_db)
    user_id = "user-rtbf-test-99"

    # 1. Default consent
    c1 = repo.dapatkan_consent(user_id)
    assert c1.izin_simpan_riwayat is True
    assert c1.durasi_simpan_hari == 90

    # 2. Update consent
    c1.izin_simpan_riwayat = False
    c1.durasi_simpan_hari = 30
    c1.topik_sensitif_diizinkan = ["duka", "trauma_ringan"]
    repo.simpan_consent(c1)

    c2 = repo.dapatkan_consent(user_id)
    assert c2.izin_simpan_riwayat is False
    assert c2.durasi_simpan_hari == 30
    assert "duka" in c2.topik_sensitif_diizinkan

    # 3. Masukkan data dummy ke tabel lain
    with get_connection(temp_db) as conn:
        conn.execute(
            "INSERT INTO mood_logs (id, user_id, waktu_iso, mood_skor, energi_skor) VALUES (?, ?, ?, ?, ?)",
            ("mood-1", user_id, "2026-11-13T10:00:00Z", 0.5, 0.7),
        )

    # 4. Right to be Forgotten
    laporan = repo.hapus_seluruh_data_user(user_id)
    assert laporan["mood_logs"] == 1
    assert laporan["consent_ledger"] == 1

    # Verifikasi data bersih
    with get_connection(temp_db) as conn:
        cur = conn.execute("SELECT COUNT(*) as cnt FROM mood_logs WHERE user_id = ?", (user_id,))
        assert cur.fetchone()["cnt"] == 0

