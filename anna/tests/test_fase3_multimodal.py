# anna/tests/test_fase3_multimodal.py — pengujian integrasi Fase 3 (Voice, Somatic, Vision, & Hard-Gate)
import pytest
from fastapi.testclient import TestClient

from anna.src.api.sse import app
from anna.src.pix.speech import siapkan_parameter_suara, bersihkan_teks_untuk_suara
from anna.src.pix.vision import ProksiVisualInput, evaluasi_visual_suportif
from anna.src.pix.breathing_widget import PengaturNapas478
from anna.src.pix.grounding_widget import Grounding54321Widget
from anna.src.storage.consent_repo import ConsentRepository, ConsentData


@pytest.fixture
def client():
    return TestClient(app)


def test_speech_config_and_cleaner():
    normal_cfg = siapkan_parameter_suara("normal")
    assert normal_cfg.rate == 0.90
    assert normal_cfg.pitch == 1.05

    krisis_cfg = siapkan_parameter_suara("krisis")
    assert krisis_cfg.rate == 0.80
    assert krisis_cfg.pitch == 1.00

    teks_kotor = "Silakan periksa [Safety Plan](https://anna.ai/plan) dan **fokus napas** ya!"
    teks_bersih = bersihkan_teks_untuk_suara(teks_kotor)
    assert "[" not in teks_bersih
    assert "https://" not in teks_bersih
    assert "**" not in teks_bersih
    assert "Safety Plan dan fokus napas ya!" in teks_bersih


def test_breathing_478_engine():
    # Detik 2: fase tarik
    s1 = PengaturNapas478.hitung_status(2.0)
    assert s1.fase == "tarik"
    assert s1.siklus_ke == 1

    # Detik 6: fase tahan (4 + 2)
    s2 = PengaturNapas478.hitung_status(6.0)
    assert s2.fase == "tahan"

    # Detik 14: fase hembus (4 + 7 + 3)
    s3 = PengaturNapas478.hitung_status(14.0)
    assert s3.fase == "hembuskan"


def test_grounding_54321_lifecycle():
    w = Grounding54321Widget()
    assert w.langkah_saat_ini().langkah == 1
    assert w.langkah_saat_ini().indra == "Penglihatan"
    assert w.langkah_saat_ini().target_jumlah == 5

    # Lanjut 4 kali
    for _ in range(4):
        selesai = w.lanjut_langkah()
        assert not selesai

    assert w.langkah_saat_ini().langkah == 5
    assert w.langkah_saat_ini().indra == "Pengecapan"

    # Lanjut ke akhir
    selesai_akhir = w.lanjut_langkah()
    assert selesai_akhir is True
    assert w.selesai is True


def test_vision_hardgate_and_consent(tmp_path):
    # 1. Hard-gate saat eskalasi ORANGE
    req_krisis = ProksiVisualInput(user_id="user-123", eskalasi="ORANGE")
    res_krisis = evaluasi_visual_suportif(req_krisis, izin_consent=True)
    assert res_krisis.status_kamera == "dimatikan_hard_gate"
    assert res_krisis.zero_biometrics_terjamin is True

    # 2. Hard-gate saat eskalasi MERAH
    req_merah = ProksiVisualInput(user_id="user-123", eskalasi="MERAH")
    res_merah = evaluasi_visual_suportif(req_merah, izin_consent=True)
    assert res_merah.status_kamera == "dimatikan_hard_gate"

    # 3. Izin ditolak saat consent False
    req_normal = ProksiVisualInput(user_id="user-123", kecerahan=0.5, eskalasi="HIJAU")
    res_tanpa_izin = evaluasi_visual_suportif(req_normal, izin_consent=False)
    assert res_tanpa_izin.status_kamera == "ditolak_tanpa_izin"

    # 4. Evaluasi pencahayaan temaram
    req_temaram = ProksiVisualInput(user_id="user-123", kecerahan=0.15, eskalasi="HIJAU")
    res_temaram = evaluasi_visual_suportif(req_temaram, izin_consent=True)
    assert res_temaram.status_kamera == "aktif"
    assert "redup" in res_temaram.observasi.lower()
    assert "lampu" in res_temaram.saran_kenyamanan.lower()


def test_api_fase3_endpoints(client, tmp_path):
    # Voice config
    resp = client.get("/api/v1/voice/config?mode=krisis")
    assert resp.status_code == 200
    assert resp.json()["rate"] == 0.80

    # Voice clean
    resp_clean = client.post("/api/v1/voice/clean", json={"teks": "**Halo** [Anna](https://a.i)"})
    assert resp_clean.status_code == 200
    assert resp_clean.json()["teks_bersih"] == "Halo Anna"

    # Vision API tanpa izin consent (default)
    u_id = "test-vis-user"
    resp_vis = client.post(
        f"/api/v1/user/{u_id}/vision",
        json={"user_id": u_id, "kecerahan": 0.5, "indikator_postur": "netral", "eskalasi": "HIJAU"}
    )
    assert resp_vis.status_code == 200
    assert resp_vis.json()["status_kamera"] == "ditolak_tanpa_izin"

