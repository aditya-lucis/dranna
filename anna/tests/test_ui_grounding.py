# anna/tests/test_ui_grounding.py — pengujian state grounding sensori 5-4-3-2-1
from anna.src.pix.grounding_widget import Grounding54321Widget


def test_grounding_tahapan():
    gw = Grounding54321Widget()
    assert gw.langkah_saat_ini().langkah == 1
    assert gw.langkah_saat_ini().target_jumlah == 5

    gw.lanjut_langkah()
    assert gw.langkah_saat_ini().langkah == 2
    assert gw.langkah_saat_ini().target_jumlah == 4

    gw.lanjut_langkah()
    gw.lanjut_langkah()
    gw.lanjut_langkah()
    assert gw.langkah_saat_ini().langkah == 5
    assert gw.langkah_saat_ini().target_jumlah == 1

    selesai = gw.lanjut_langkah()
    assert selesai is True
    assert gw.selesai is True


def test_grounding_reset():
    gw = Grounding54321Widget()
    gw.lanjut_langkah()
    gw.reset()
    assert gw.langkah_saat_ini().langkah == 1
    assert gw.selesai is False
