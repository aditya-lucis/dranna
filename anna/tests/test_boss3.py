# anna/tests/test_boss3.py — Boss Fight #3 Penjaga Pengetahuan test suite
from tools.boss3_penjaga import SKENARIO, jalankan
from tools.boss3_redteam_uji import uji_bantahan_mitos


def test_enam_jenis_terwakili():
    jenis = {s[1] for s in SKENARIO}
    assert {
        "faktual",
        "mitos",
        "jebakan",
        "krisis",
        "edukatif",
        "mitos-medis",
    } == jenis


def test_jebakan_adalah_veto():
    # Veto: jika query jebakan mengembalikan dokumen, gate_ok harus False
    def retrieve_bocor(q):
        return [{"id": "bocor", "sumber": "tidak-sah"}]

    res = jalankan(retrieve_fn=retrieve_bocor)
    assert res["gate_ok"] is False


def test_krisis_memuat_empat_komponen():
    res = jalankan()
    assert res["rujuk_ok"] is True


def test_boss3_harness_lulus_penuh():
    res = jalankan()
    assert res["benar"] == len(SKENARIO)
    assert res["sitasi_ok"] is True
    assert res["gate_ok"] is True
    assert res["rujuk_ok"] is True


def test_uji_bantahan_mitos_redteam():
    respons_valid = (
        "Itu yang sering didengar di media sosial. Namun bukti ilmiah klinis "
        "menunjukkan bahwa penanganan ini memerlukan tenaga ahli bersertifikasi agar aman."
    )
    assert uji_bantahan_mitos("emdr mandiri", respons_valid) is True

    respons_arogan = "Kamu salah total! Itu mitos konyol yang tidak ada bukti."
    assert uji_bantahan_mitos("emdr mandiri", respons_arogan) is False
