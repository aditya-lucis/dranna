# anna/tests/test_tidur.py
from anna.src.piii.tidur import refleksi_tidur


def test_sehat_simpan():
    assert "simpan" in refleksi_tidur({
        "ritme_konsisten": 1,
        "kamar_dingin_gelap": 1,
        "tanpa_layar_60m": 1,
        "kafein_setelah_14": 1,
        "olahraga_siang": 1,
    })


def test_insomnia_kronik_rujuk_cbt_i():
    r = refleksi_tidur({"insomnia_berbulan": True})
    assert "CBT-I" in r or "profesional" in r


def test_tak_ada_perintah_8_jam():
    for v in [{"ritme_konsisten": 0}, {"kamar_dingin_gelap": 1}]:
        assert "8 jam" not in refleksi_tidur(v)
