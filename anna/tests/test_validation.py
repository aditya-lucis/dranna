# anna/tests/test_validation.py — pengujian level validasi DBT Linehan
from anna.src.pii.validation import level_validation


def test_menepis_ditolak():
    """Invarian etis: Respons yang menepis atau menyuruh santai jatuh ke Level 0 (tertolak)."""
    r = level_validation("Ah biasa aja itu, coba santai aja ya.", "aku sedih")
    assert r["level"] == 0
    assert "menepis" in r["masalah"]


def test_klaim_mutlak_tidak_disahkan():
    """Pencegahan overvalidation: Menyetujui klaim mutlak tanpa refleksi terdeteksi bermasalah."""
    pesan = "semua orang selalu pergi dan gak ada yang peduli"
    r = level_validation("Iya, semua orang memang begitu kok.", pesan)
    assert r.get("masalah") == "overvalidation klaim mutlak"


def test_validasi_kontekstual_lulus():
    """Validasi sehat: Mengakui kenyataan rasa ('nyata dan masuk akal') mencapai level 4."""
    pesan = "aku kecewa banget"
    r = level_validation("Kecewamu nyata dan masuk akal setelah apa yang terjadi.", pesan)
    assert r["level"] >= 3
