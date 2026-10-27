# anna/tests/test_krisis_shutdown.py — pengujian protokol hard persona shutdown
from anna.src.pvi.shutdown import PersonaShutdown


def test_shutdown_harus_bungkam():
    assert PersonaShutdown.harus_dibungkam("RED") is True
    assert PersonaShutdown.harus_dibungkam("ORANGE") is True
    assert PersonaShutdown.harus_dibungkam("YELLOW") is False
    assert PersonaShutdown.harus_dibungkam("GREEN") is False


def test_terapkan_shutdown_persona():
    assert PersonaShutdown.terapkan_shutdown("waifu", "RED") == "netral-tenang"
    assert PersonaShutdown.terapkan_shutdown("sister", "ORANGE") == "netral-tenang"
    assert PersonaShutdown.terapkan_shutdown("waifu", "GREEN") == "waifu"


def test_sensor_kata_terlarang():
    res = PersonaShutdown.verifikasi_output("jangan sedih ya sayang, aku di sini", "RED")
    assert res["lulus"] is False
    assert "sayang" in res["pelanggaran"]


def test_pembersihan_output():
    teks = "tenang ya sayang, kamu aman."
    bersih = PersonaShutdown.bersihkan_output(teks)
    assert "sayang" not in bersih
    assert "tenang ya" in bersih
