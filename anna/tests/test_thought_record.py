# anna/tests/test_thought_record.py
from anna.src.piv.thought_record import prompt_kolom, KOLOM, mulai_thought_record, lanjut_kolom


def test_lima_kolom():
    assert len(KOLOM) == 5


def test_kolom_emosi_minta_persen():
    assert "0-100" in prompt_kolom(2) or "100" in prompt_kolom(2)


def test_alat_langchain():
    p0 = mulai_thought_record.invoke({})
    assert "Situasi" in p0
    p1 = lanjut_kolom.invoke({"i": 0, "jawaban": "Ditolak tawaran"})
    assert "Pikiran" in p1
