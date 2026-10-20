# anna/tests/test_korpus.py
import pytest
from pydantic import ValidationError
from anna.src.piii.korpus import DokumenPsy


def test_dokumen_tanpa_sumber_ditolak():
    with pytest.raises(ValidationError):
        DokumenPsy(
            id="test-01",
            topik="anxietas",
            subtopik="tes",
            tingkat_bukti="kuat",
            ringkas="Ringkasan singkat.",
            isi="Isi penjelasan.",
            sumber="",  # Sumber kosong harus ditolak (min_length=8)
            tahun_review=2026,
        )


def test_materi_tua_turun_prioritas():
    dok_baru = DokumenPsy(
        id="baru-01",
        topik="anxietas",
        subtopik="tes",
        tingkat_bukti="kuat",
        ringkas="Ringkasan.",
        isi="Isi.",
        sumber="NIMH Anxiety Guidelines",
        tahun_review=2026,
    )
    dok_lama = DokumenPsy(
        id="lama-01",
        topik="anxietas",
        subtopik="tes",
        tingkat_bukti="kuat",
        ringkas="Ringkasan.",
        isi="Isi.",
        sumber="NIMH Anxiety Guidelines",
        tahun_review=2022,  # > 24 bulan
    )
    assert dok_baru.prioritas(2026) == 1.0
    assert dok_lama.prioritas(2026) == 0.60
    assert dok_baru.prioritas(2026) > dok_lama.prioritas(2026)
