# anna/tests/test_etika_pii.py — pengujian sanitasi & redaksi PII
from anna.src.pvii.pii import SanitizerPII, redaksi_pii


def test_redaksi_nik():
    teks = "NIK saya adalah 3171012345678901 untuk verifikasi."
    bersih, entitas = SanitizerPII.redaksi(teks)
    assert "[TEREDAKSI-NIK]" in bersih
    assert "3171012345678901" not in bersih
    assert "NIK" in entitas


def test_redaksi_nomor_hp():
    teks = "Hubungi saya di 081298765432 atau +6281122334455."
    bersih, entitas = SanitizerPII.redaksi(teks)
    assert "[TEREDAKSI-HP]" in bersih
    assert "081298765432" not in bersih
    assert "NOMOR_HP" in entitas


def test_redaksi_email():
    teks = "Kirim ke pasien@konseling-mental.id segera."
    bersih = redaksi_pii(teks)
    assert "[TEREDAKSI-EMAIL]" in bersih
    assert "pasien@konseling-mental.id" not in bersih


def test_teks_tanpa_pii_tidak_berubah():
    teks = "Saya merasa cemas saat presentasi di depan kelas."
    bersih, entitas = SanitizerPII.redaksi(teks)
    assert bersih == teks
    assert len(entitas) == 0
