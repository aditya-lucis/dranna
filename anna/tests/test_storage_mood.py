# anna/tests/test_storage_mood.py — pengujian unit repositori mood & deteksi flatline >= 7 hari
import os
import tempfile
from pathlib import Path
import pytest
from anna.src.storage.mood_repo import MoodRepository
from anna.src.pix.journal import CatatanJurnal
from fastapi.testclient import TestClient
from anna.src.api.sse import app

client = TestClient(app)


@pytest.fixture
def temp_repo():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        path = Path(f.name)
    repo = MoodRepository(db_path=path)
    yield repo
    try:
        os.remove(path)
    except Exception:
        pass


def test_mood_simpan_dan_riwayat(temp_repo):
    user_id = "user-mood-01"
    c1 = CatatanJurnal(
        id="m1",
        waktu_iso="2026-11-01T10:00:00Z",
        mood_skor=0.6,
        energi_skor=0.75,
        catatan_refleksi="Hari yang produktif.",
        hal_yang_disyukuri=["Kopi", "Udara sejuk"],
    )
    temp_repo.simpan_catatan(user_id, c1)

    riwayat = temp_repo.ambil_riwayat(user_id)
    assert len(riwayat) == 1
    assert riwayat[0].mood_skor == 0.6
    assert "Kopi" in riwayat[0].hal_yang_disyukuri


def test_deteksi_flatline_7_hari(temp_repo):
    """Pengujian Kondisi Wajib Berhenti #4: mood datar <= -0.5 selama 7 hari berturut-turut."""
    user_id = "user-flatline-02"

    # Masukkan 7 entri berat berturut-turut tanpa pemulihan
    for i in range(1, 8):
        c = CatatanJurnal(
            id=f"flat-{i}",
            waktu_iso=f"2026-11-0{i}T12:00:00Z",
            mood_skor=-0.7,
            energi_skor=0.2,
            catatan_refleksi="Tetap hampa dan tidak ada energi.",
            hal_yang_disyukuri=[],
        )
        temp_repo.simpan_catatan(user_id, c)

    analisis = temp_repo.analisis_flatline(user_id, ambang_hari=7)
    assert analisis.total_entri == 7
    assert analisis.flatline_terdeteksi is True
    assert analisis.rekomendasi_rujukan is True
    assert "7 hari berturut-turut" in analisis.pesan_evaluasi
    assert "psikolog" in analisis.pesan_evaluasi or "psikiater" in analisis.pesan_evaluasi


def test_mood_fluktuatif_tidak_flatline(temp_repo):
    """Pola mood yang naik-turun wajar tidak boleh salah memicu flatline."""
    user_id = "user-normal-03"
    skor_list = [-0.6, 0.2, -0.4, 0.5, -0.2, 0.3, -0.5]
    for i, s in enumerate(skor_list, 1):
        c = CatatanJurnal(
            id=f"norm-{i}",
            waktu_iso=f"2026-11-0{i}T12:00:00Z",
            mood_skor=s,
            energi_skor=0.6,
            catatan_refleksi="Hari biasa.",
            hal_yang_disyukuri=["Teman"],
        )
        temp_repo.simpan_catatan(user_id, c)

    analisis = temp_repo.analisis_flatline(user_id, ambang_hari=7)
    assert analisis.flatline_terdeteksi is False
    assert analisis.rekomendasi_rujukan is False


def test_api_journal_endpoints():
    user_id = "user-api-journal-99"
    payload = {
        "id": "j-api-1",
        "waktu_iso": "2026-11-13T12:00:00Z",
        "mood_skor": 0.4,
        "energi_skor": 0.8,
        "catatan_refleksi": "Uji integrasi API jurnal.",
        "hal_yang_disyukuri": ["Kesehatan", "Keluarga"],
    }
    # 1. POST
    res_post = client.post(f"/api/v1/user/{user_id}/journal", json=payload)
    assert res_post.status_code == 200
    assert res_post.json()["status"] == "tersimpan"

    # 2. GET
    res_get = client.get(f"/api/v1/user/{user_id}/journal")
    assert res_get.status_code == 200
    data = res_get.json()
    assert len(data["riwayat"]) >= 1
    assert data["analisis"]["total_entri"] >= 1
