# anna/tests/test_ekspresi.py — pengujian avatar status UI tanpa kepura-puraan
from anna.src.pii.ekspresi import EKSPRESI, TRANSISI, ekspresi_untuk


def test_semua_ekspresi_punya_padanan_teks():
    """Invarian aksesibilitas: Semua ekspresi visual memiliki teks alternatif non-kosong."""
    for e in EKSPRESI.values():
        assert len(e.padanan_teks) >= 3


def test_mode_tenang_meredam():
    """Kontrak visual krisis: Saat keselamatan aktif ('tenang'), ekspresi animasi ceria diredam ke 'tenang'."""
    assert ekspresi_untuk("menulis", "tenang").nama == "tenang"


def test_maksimal_tujuh_ekspresi():
    """Anggaran ekspresi: Maksimal 7 state ekspresi yang jelas dan dapat diaudit."""
    assert len(EKSPRESI) <= 7
