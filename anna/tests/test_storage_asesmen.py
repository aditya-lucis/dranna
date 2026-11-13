# anna/tests/test_storage_asesmen.py — pengujian unit asesmen PHQ-9 & GAD-7 serta killswitch Item-9
import os
import tempfile
from pathlib import Path
import pytest
from anna.src.klinik.gad7 import skor_gad7
from anna.src.klinik.pertanyaan_asesmen import dapatkan_paket_asesmen
from anna.src.storage.asesmen_repo import AsesmenRepository, AsesmenSubmit
from fastapi.testclient import TestClient
from anna.src.api.sse import app

client = TestClient(app)


@pytest.fixture
def temp_repo():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        path = Path(f.name)
    repo = AsesmenRepository(db_path=path)
    yield repo
    try:
        os.remove(path)
    except Exception:
        pass


def test_gad7_skor_kategori():
    # 7 butir: total 0
    res0 = skor_gad7([0, 0, 0, 0, 0, 0, 0])
    assert res0["total"] == 0
    assert res0["kategori"] == "minimal"
    assert res0["kategori_adalah_diagnosis"] is False

    # total 7 -> ringan
    res7 = skor_gad7([1, 1, 1, 1, 1, 1, 1])
    assert res7["total"] == 7
    assert res7["kategori"] == "ringan"

    # total 18 -> berat
    res18 = skor_gad7([3, 3, 3, 3, 2, 2, 2])
    assert res18["total"] == 18
    assert res18["kategori"] == "berat"


def test_paket_pertanyaan():
    p_phq = dapatkan_paket_asesmen("phq9")
    assert len(p_phq["pertanyaan"]) == 9
    assert p_phq["pertanyaan"][8]["is_item9"] is True

    p_gad = dapatkan_paket_asesmen("gad7")
    assert len(p_gad["pertanyaan"]) == 7

    with pytest.raises(ValueError):
        dapatkan_paket_asesmen("invalid_test")


def test_asesmen_phq9_item9_killswitch(temp_repo):
    """Memastikan Item-9 positif seketika memicu rujukan darurat krisis + hotline."""
    user_id = "user-phq9-item9-alert"
    # Butir ke-9 dijawab 2 (lebih dari separuh waktu pikiran menyakiti diri)
    submit = AsesmenSubmit(
        jenis="phq9",
        jawaban=[1, 1, 0, 1, 0, 1, 0, 0, 2],
        geo="id",
    )
    rec = temp_repo.proses_dan_simpan(user_id, submit)
    assert rec.item9_positif is True
    assert rec.krisis_darurat is True
    assert rec.pesan_rujukan is not None
    assert "119" in rec.pesan_rujukan
    assert len(rec.hotlines) >= 1
    assert rec.kategori_adalah_diagnosis is False


def test_asesmen_normal_tersimpan(temp_repo):
    user_id = "user-normal-eval"
    submit = AsesmenSubmit(
        jenis="gad7",
        jawaban=[0, 1, 0, 1, 0, 0, 1],
        geo="id",
    )
    rec = temp_repo.proses_dan_simpan(user_id, submit)
    assert rec.krisis_darurat is False
    assert rec.skor_total == 3
    assert rec.kategori == "minimal"

    riwayat = temp_repo.ambil_riwayat(user_id)
    assert len(riwayat) == 1
    assert riwayat[0].jenis_asesmen == "gad7"


def test_api_asesmen_endpoints():
    # 1. GET Pertanyaan
    res_q = client.get("/api/v1/asesmen/pertanyaan/phq9")
    assert res_q.status_code == 200
    assert len(res_q.json()["pertanyaan"]) == 9

    # 2. POST Submit
    user_id = "user-api-asesmen-99"
    payload = {
        "jenis": "gad7",
        "jawaban": [1, 2, 1, 2, 1, 1, 1],
        "geo": "id",
    }
    res_sub = client.post(f"/api/v1/user/{user_id}/asesmen", json=payload)
    assert res_sub.status_code == 200
    assert res_sub.json()["skor_total"] == 9
    assert res_sub.json()["kategori"] == "ringan"

    # 3. GET Riwayat
    res_hist = client.get(f"/api/v1/user/{user_id}/asesmen")
    assert res_hist.status_code == 200
    assert len(res_hist.json()["riwayat"]) >= 1

