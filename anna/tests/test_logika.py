# anna/tests/test_logika.py — pengujian formal logika proposisi keselamatan
import itertools
from anna.src.pi.logika import (
    aturan_kamera_boleh,
    aturan_persona_off,
    aturan_perlu_verifikasi,
    audit_invarian_persona,
)


def test_kamera_butuh_semua_komponen():
    """Hukum De Morgan: Kamera menyala HANYA jika semua komponen persetujuan terpenuhi."""
    for vals in itertools.product([False, True], repeat=3):
        S = {"persetujuan": dict(zip(["tujuan", "durasi", "pencabutan"], vals))}
        assert aturan_kamera_boleh(S) == all(vals)


def test_persona_off_menutup_semua_jalan():
    """Invarian keselamatan: Bila ada bukti eksplisit atau level RED, persona wajib nonaktif."""
    for bukti, level in itertools.product(
        [False, True], ["GREEN", "YELLOW", "ORANGE", "RED"]
    ):
        S = {"bukti_eksplisit": bukti, "level": level}
        if bukti or level == "RED":
            assert aturan_persona_off(S) is True


def test_sudah_dijawab_mematikan_verifikasi():
    """Short-circuit: Pengguna yang sudah menjawab verifikasi tidak dicecar pertanyaan ulang."""
    S = {"kata_parah": True, "pola_waktu": True, "sudah_dijawab": True}
    assert aturan_perlu_verifikasi(S) is False


def test_audit_invarian_terjaga():
    """Uji exhaustive: Evaluasi kontraposisi aturan persona lolos 100%."""
    assert audit_invarian_persona() is True
