# anna/tests/test_storage_safety_plan.py — pengujian unit Safety Plan Stanley-Brown & Memori Episodik Zero-PII
import os
import tempfile
from pathlib import Path
import pytest
from anna.src.storage.safety_plan_repo import SafetyPlanRepository, SafetyPlanModel, KontakItem
from anna.src.storage.episodic_repo import EpisodicRepository
from fastapi.testclient import TestClient
from anna.src.api.sse import app

client = TestClient(app)


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        path = Path(f.name)
    yield path
    try:
        os.remove(path)
    except Exception:
        pass


def test_safety_plan_default_dan_simpan(temp_db):
    repo = SafetyPlanRepository(db_path=temp_db)
    user_id = "user-safety-01"

    # 1. Ambil default
    p_def = repo.ambil_safety_plan(user_id, geo="id")
    assert len(p_def.tanda_peringatan) >= 2
    assert len(p_def.strategi_koping) >= 2
    assert any("119" in k.kontak_info for k in p_def.kontak_profesional)

    # 2. Modifikasi dan simpan
    p_def.tanda_peringatan.append("Mulai malas makan")
    p_def.kontak_personal.append(
        KontakItem(nama="Kakak", kontak_info="081234567890", keterangan="Kakak kandung")
    )
    saved = repo.simpan_safety_plan(p_def)
    assert len(saved.tanda_peringatan) == 4

    # 3. Reload
    p_re = repo.ambil_safety_plan(user_id, geo="id")
    assert len(p_re.tanda_peringatan) == 4
    assert any(k.nama == "Kakak" for k in p_re.kontak_personal)


def test_episodic_memory_sanitasi_pii(temp_db):
    repo = EpisodicRepository(db_path=temp_db)
    user_id = "user-episodic-02"

    teks_dengan_pii = (
        "Pengguna bercerita tentang stres kerja, nomor HP dia 081234567890 "
        "dan NIK 3171012345670001 saat pendaftaran."
    )
    mem = repo.simpan_memori(
        user_id=user_id,
        sesi_id="sesi-ep-1",
        topik="stres_kerja",
        ringkasan=teks_dengan_pii,
        valence=-0.4,
        teknik="breathing_478",
    )

    # Verifikasi Zero-PII
    assert "081234567890" not in mem.ringkasan_konteks
    assert "3171012345670001" not in mem.ringkasan_konteks
    assert "[TEREDAKSI-HP]" in mem.ringkasan_konteks
    assert "[TEREDAKSI-NIK]" in mem.ringkasan_konteks

    # Verifikasi recall
    konteks = repo.bangun_konteks_ringkasan(user_id)
    assert "stres_kerja" in konteks


def test_api_safety_plan_dan_memory():
    user_id = "user-api-safety-plan-99"

    # 1. GET Safety Plan
    res_sp = client.get(f"/api/v1/user/{user_id}/safety-plan")
    assert res_sp.status_code == 200
    assert len(res_sp.json()["tanda_peringatan"]) >= 1

    # 2. POST Memory
    payload_mem = {
        "sesi_id": "sesi-uji-api-99",
        "topik": "kecemasan_malam",
        "ringkasan": "Klien merasa cemas karena beban tugas akhir.",
        "valence": -0.3,
        "teknik": "cbt_thought_record",
    }
    res_mem = client.post(f"/api/v1/user/{user_id}/memory", json=payload_mem)
    assert res_mem.status_code == 200
    assert res_mem.json()["status"] == "tersimpan"

    # 3. GET Memory
    res_mem_get = client.get(f"/api/v1/user/{user_id}/memory")
    assert res_mem_get.status_code == 200
    assert len(res_mem_get.json()["memori"]) >= 1

