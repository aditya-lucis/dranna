# anna/tests/test_anxietas.py
from anna.src.piii.anxietas import KORPUS_ANX, tawarkan_skrining_gad7


def test_korpus_anxietas_punya_dua_dokumen_berlabel():
    assert len(KORPUS_ANX) == 2
    assert all(d.sumber and d.tahun_review for d in KORPUS_ANX)


def test_tawaran_hanya_setelah_berulang():
    sesi = {"log": [{"topik": "anxietas"}] * 3, "gad7_ditawarkan": False}
    assert tawarkan_skrining_gad7(sesi) is not None
    sesi2 = {"log": [{"topik": "anxietas"}], "gad7_ditawarkan": False}
    assert tawarkan_skrining_gad7(sesi2) is None
