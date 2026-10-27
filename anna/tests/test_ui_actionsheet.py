# anna/tests/test_ui_actionsheet.py — pengujian Crisis Action Sheet generator
from anna.src.pix.action_sheet import CrisisActionSheet


def test_action_sheet_indonesia():
    kontak = CrisisActionSheet.dapatkan_aksi_cepat("id")
    assert len(kontak) >= 3
    uris = [k.uri_aksi for k in kontak]
    assert "tel:119" in uris
    assert "tel:110" in uris
    assert "tel:112" in uris


def test_action_sheet_global():
    kontak = CrisisActionSheet.dapatkan_aksi_cepat("us")
    uris = [k.uri_aksi for k in kontak]
    assert "tel:988" in uris
