# anna/tests/test_korpus_audit.py
from tools.korpus_audit import audit_korpus


def test_korpus_sehat_lolos():
    k = [
        {
            "id": "x",
            "sumber": "NIMH Anxiety Guidelines",
            "reviewer": "dr Spesialis Jiwa",
            "tahun_review": 2026,
            "tingkat_bukti": "kuat",
        }
    ]
    assert audit_korpus(k)["lolos"] is True


def test_tanpa_sumber_ditangkap():
    k = [
        {
            "id": "x",
            "sumber": "",
            "reviewer": "dr",
            "tahun_review": 2026,
            "tingkat_bukti": "moderat",
        }
    ]
    assert audit_korpus(k)["lolos"] is False


def test_usia_tua_ditangkap():
    k = [
        {
            "id": "x",
            "sumber": "NIMH",
            "reviewer": "dr",
            "tahun_review": 2022,
            "tingkat_bukti": "moderat",
        }
    ]
    assert audit_korpus(k)["lolos"] is False
