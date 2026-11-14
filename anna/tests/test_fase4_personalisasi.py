# anna/tests/test_fase4_personalisasi.py — pengujian Fase 4 (Style Governor v2, Homework, & PCA Pattern)
import pytest
from fastapi.testclient import TestClient

from anna.src.api.sse import app
from anna.src.agent.governor_v2 import StyleGovernorV2, StyleConfig
from anna.src.storage.homework_repo import HomeworkRepository
from anna.src.storage.consent_repo import ConsentRepository
from anna.src.storage.mood_repo import MoodRepository
from anna.src.klinik.pola_longitudinal import DetektorPolaLongitudinal
from anna.src.pix.journal import CatatanJurnal


@pytest.fixture
def client():
    return TestClient(app)


def test_governor_v2_hardgate():
    # Hard-gate eskalasi ORANGE
    gov = StyleGovernorV2(config=StyleConfig(user_id="u1", preferensi_gaya="ringan_playful", persona="waifu"))
    res = gov.evaluasi_gaya(eskalasi="ORANGE")
    assert res.gaya_aktif == "netral-tenang"
    assert res.sumber_keputusan == "hard_gate"

    # Hard-gate eskalasi RED
    res_red = gov.evaluasi_gaya(eskalasi="RED")
    assert res_red.gaya_aktif == "netral-tenang"
    assert res_red.sumber_keputusan == "hard_gate"


def test_governor_v2_explicit_preference():
    # Preferensi eksplisit mengalahkan kepribadian atau persona
    gov = StyleGovernorV2(config=StyleConfig(user_id="u1", preferensi_gaya="validasi_dahulu", persona="waifu"))
    res = gov.evaluasi_gaya(eskalasi="GREEN")
    assert res.gaya_aktif == "validasi_dahulu"
    assert res.sumber_keputusan == "preferensi_eksplisit"

    gov2 = StyleGovernorV2(config=StyleConfig(user_id="u1", preferensi_gaya="terstruktur_fokus", persona="sister"))
    res2 = gov2.evaluasi_gaya(eskalasi="GREEN")
    assert res2.gaya_aktif == "terstruktur_fokus"
    assert res2.sumber_keputusan == "preferensi_eksplisit"


def test_governor_v2_auto_fallback():
    # Mode auto tanpa riwayat pesan -> fallback ke persona
    gov_waifu = StyleGovernorV2(config=StyleConfig(user_id="u1", preferensi_gaya="auto", persona="waifu"))
    res_waifu = gov_waifu.evaluasi_gaya(eskalasi="GREEN", riwayat_pesan=[])
    assert res_waifu.gaya_aktif == "ringan_playful"
    assert res_waifu.sumber_keputusan == "default_persona"

    gov_sister = StyleGovernorV2(config=StyleConfig(user_id="u1", preferensi_gaya="auto", persona="sister"))
    res_sister = gov_sister.evaluasi_gaya(eskalasi="GREEN", riwayat_pesan=[])
    assert res_sister.gaya_aktif == "pendengar_tenang"


def test_homework_lifecycle(tmp_path):
    db_file = tmp_path / "test_hw.db"
    repo = HomeworkRepository(db_path=db_file)
    u_id = "user-hw-1"

    # 1. Tambah tugas
    t1 = repo.tambah_tugas(u_id, "napas", "Latihan pernapasan 4-7-8 selama 3 menit sore ini")
    t2 = repo.tambah_tugas(u_id, "values", "Tulis 1 komitmen kecil terkait keluarga")
    assert t1.id.startswith("hw-")
    assert t1.status == "pending"

    # 2. Ambil pending
    pending = repo.ambil_tugas_pending(u_id)
    assert len(pending) == 2

    # 3. Bangun ringkasan awal sesi
    ringkasan = repo.bangun_ringkasan_homework_awal_sesi(u_id)
    assert "TUGAS MIKRO" in ringkasan
    assert "Latihan pernapasan" in ringkasan
    assert "tanpa menghakimi" in ringkasan

    # 4. Selesaikan tugas 1
    sukses = repo.perbarui_status(t1.id, u_id, status="selesai", refleksi="Merasa jauh lebih tenang")
    assert sukses is True

    # 5. Cek sisa pending
    pending_after = repo.ambil_tugas_pending(u_id)
    assert len(pending_after) == 1
    assert pending_after[0].id == t2.id

    # 6. RTBF: Hapus total data pengguna
    c_repo = ConsentRepository(db_path=db_file)
    laporan = c_repo.hapus_seluruh_data_user(u_id)
    assert laporan.get("homework_tasks", 0) == 2
    assert len(repo.ambil_riwayat_tugas(u_id)) == 0


def test_pola_longitudinal_pca_and_mad(tmp_path):
    db_file = tmp_path / "test_pola.db"
    mood_repo = MoodRepository(db_path=db_file)
    detektor = DetektorPolaLongitudinal(db_path=db_file)
    u_id = "user-pola-1"

    # Belum cukup data (< 3 hari)
    res_awal = detektor.analisis_pengguna(u_id)
    assert res_awal.cukup_data is False
    assert res_awal.total_hari == 0

    # Isi 5 hari data mood
    for day in range(1, 6):
        mood_repo.simpan_catatan(
            u_id,
            CatatanJurnal(
                id=f"m-{day}",
                waktu_iso=f"2026-11-0{day}T10:00:00Z",
                mood_skor=0.4 if day != 4 else -0.8,  # Hari 4 anomali penurunan tajam
                energi_skor=0.6 if day != 4 else 0.1,
                catatan_refleksi="Hari biasa" if day != 4 else "Sangat lelah dan tertekan",
                hal_yang_disyukuri=["Kopi"] if day != 4 else [],
            ),
        )

    # Analisis setelah 5 hari
    res_analisis = detektor.analisis_pengguna(u_id)
    assert res_analisis.cukup_data is True
    assert res_analisis.total_hari == 5
    assert len(res_analisis.titik_proyeksi) == 5
    assert len(res_analisis.rasio_variansi) > 0


def test_api_fase4_endpoints(client):
    u_id = "test-f4-api"

    # 1. Style API
    resp_style = client.get(f"/api/v1/user/{u_id}/style")
    assert resp_style.status_code == 200

    resp_set_style = client.post(
        f"/api/v1/user/{u_id}/style",
        json={"user_id": u_id, "preferensi_gaya": "terstruktur_fokus", "persona": "sister"}
    )
    assert resp_set_style.status_code == 200
    assert resp_set_style.json()["evaluasi"]["gaya_aktif"] == "terstruktur_fokus"

    # 2. Homework API
    resp_add_hw = client.post(
        f"/api/v1/user/{u_id}/homework",
        json={"kategori": "napas", "deskripsi": "Latihan 4-7-8 sebelum rapat"}
    )
    assert resp_add_hw.status_code == 200
    task_id = resp_add_hw.json()["tugas"]["id"]

    resp_get_hw = client.get(f"/api/v1/user/{u_id}/homework?pending_only=true")
    assert resp_get_hw.status_code == 200
    assert len(resp_get_hw.json()["tugas"]) >= 1

    resp_patch_hw = client.patch(
        f"/api/v1/user/{u_id}/homework/{task_id}",
        json={"status": "selesai", "refleksi": "Bagus sekali"}
    )
    assert resp_patch_hw.status_code == 200

    # 3. Pattern Insights API
    resp_pola = client.get(f"/api/v1/user/{u_id}/insights/pattern")
    assert resp_pola.status_code == 200
    assert "cukup_data" in resp_pola.json()

