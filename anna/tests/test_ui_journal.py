# anna/tests/test_ui_journal.py — pengujian model & manajer jurnal emosi
from anna.src.pix.journal import JurnalEmosi, CatatanJurnal


def test_jurnal_simpan_dan_rata_rata():
    jurnal = JurnalEmosi()
    c1 = CatatanJurnal(
        id="c1",
        waktu_iso="2026-10-27T10:00:00",
        mood_skor=0.5,
        energi_skor=0.8,
        catatan_refleksi="Hari yang menyenangkan.",
        hal_yang_disyukuri=["Teman", "Kesehatan"],
    )
    c2 = CatatanJurnal(
        id="c2",
        waktu_iso="2026-10-27T20:00:00",
        mood_skor=0.3,
        energi_skor=0.6,
        catatan_refleksi="Malam yang tenang.",
        hal_yang_disyukuri=["Secangkir teh"],
    )
    jurnal.simpan(c1)
    jurnal.simpan(c2)

    assert jurnal.total() == 2
    assert jurnal.rata_rata_mood() == 0.4
    assert len(jurnal.ambil_riwayat(limit=1)) == 1
