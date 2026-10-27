# anna/tests/test_ui_speech.py — pengujian konfigurasi TTS & pembersihan markdown vokal
from anna.src.pix.speech import siapkan_parameter_suara, bersihkan_teks_untuk_suara


def test_vokal_normal():
    cfg = siapkan_parameter_suara("normal")
    assert cfg.rate == 0.90
    assert cfg.pitch == 1.05
    assert cfg.mode == "normal"


def test_vokal_krisis():
    cfg = siapkan_parameter_suara("krisis")
    assert cfg.rate == 0.80
    assert cfg.pitch == 1.00
    assert cfg.mode == "krisis"


def test_bersihkan_teks_markdown():
    teks = "**Halo** [Anna](https://anna.ai), coba _tarik napas_ perlahan."
    bersih = bersihkan_teks_untuk_suara(teks)
    assert "**" not in bersih
    assert "_" not in bersih
    assert "https://" not in bersih
    assert "Halo Anna, coba tarik napas perlahan." == bersih
