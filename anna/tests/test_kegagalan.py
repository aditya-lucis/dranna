# anna/tests/test_kegagalan.py — pengujian detektor anti-pattern empati & korpus kegagalan
import json
from pathlib import Path
from anna.src.pii.kegagalan import deteksi_kegagalan


def test_lima_pelanggaran_tertangkap():
    """Anti-pattern: Lima kategori kegagalan empati utama tertangkap dan ditolak."""
    uji = [
        "Yang penting sehat ya, bersyukur aja!",
        "Setidaknya kamu masih punya pekerjaan.",
        "Tidak seburuk itu kok, kamu cuma overthinking.",
        "Coba meditasi tiap pagi pasti membaik.",
        "Masih ada yang lebih parah kok.",
    ]
    for t in uji:
        assert deteksi_kegagalan(t)["tindakan"] == "tolak-dan-rewrite", t


def test_validasi_murni_lulus():
    """Validasi sehat: Kalimat pengakuan yang jujur dan kontekstual lulus tanpa hambatan."""
    t = "Kelelahanmu nyata. Masuk akal setelah minggu begini."
    assert deteksi_kegagalan(t)["tindakan"] == "lulus"


def test_gaslighting_struktural():
    """Invarian keselamatan: Mengutip kenaikan skor numerik tanpa validasi emosional dilarang."""
    r = deteksi_kegagalan(
        "Skormu naik minggu ini.",
        {"skor_disebut": True, "pernyataan_dukungan": False},
    )
    assert any(j == "gaslighting" for j, _ in r["pola"])


def test_korpus_kegagalan_anti_pattern():
    """Uji korpus 20 contoh: 12 pelanggaran wajib tertangkap (100% recall), 8 kalimat sah 0 false positive."""
    korpus_path = Path(__file__).parent / "korpus_kegagalan.json"
    data = json.loads(korpus_path.read_text(encoding="utf-8"))

    # 12 pelanggaran harus ditolak
    for item in data["pelanggaran"]:
        res = deteksi_kegagalan(item["teks"])
        assert res["tindakan"] == "tolak-dan-rewrite", f"Gagal menangkap: {item['teks']}"

    # 8 kalimat mirip tapi sah harus lulus (0 false positive)
    for item in data["mirip_tapi_sah"]:
        res = deteksi_kegagalan(item["teks"])
        assert res["tindakan"] == "lulus", f"False positive pada kalimat sah: {item['teks']}"
