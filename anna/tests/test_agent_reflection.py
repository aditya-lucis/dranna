# anna/tests/test_agent_reflection.py — pengujian node refleksi etika pra-streaming
from anna.src.agent.reflection import evaluasi_dan_perbaiki


def test_reflection_respons_bersih_lolos():
    draft = "Wajar bila kamu merasa lelah hari ini. Kita bisa pelan-pelan istirahat."
    res = evaluasi_dan_perbaiki(draft)
    assert res["lolos"] is True
    assert res["respons_final"] == draft


def test_reflection_trauma_detail_dicegat():
    draft = "Jelaskan detailnya apa yang terjadi saat peristiwa kekerasan itu."
    res = evaluasi_dan_perbaiki(draft)
    assert res["lolos"] is False
    assert "trauma_detail_diminta" in res["masalah"]
    assert "Kita tidak harus membuka apa pun hari ini" in res["respons_final"]


def test_reflection_duka_klise_dicegat():
    draft = "Kamu sedang di tahap tawar-menawar duka, ikhlaskan saja."
    res = evaluasi_dan_perbaiki(draft)
    assert res["lolos"] is False
    assert "Kehilangan ini nyata dan berat" in res["respons_final"]


def test_reflection_toxic_positivity_dicegat():
    draft = "Semua pasti ada hikmahnya! Jangan sedih, selalu berpikir positif ya!"
    res = evaluasi_dan_perbaiki(draft)
    assert res["lolos"] is False
    assert "toxic_positivity" in res["masalah"]
    assert "Ini situasi yang tidak mudah" in res["respons_final"]
