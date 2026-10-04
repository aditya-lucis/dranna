# anna/tests/test_chunk.py — pengujian semantic chunking dan safety buffer gate
from anna.src.pii.chunk import gate_chunk, potong_chunk


def test_potong_di_batas_napas():
    """Chunking semantik: Teks dipotong pada batas tanda baca napas, bukan kata acak."""
    teks = "Hari berat ya. Kubaca lelahmu. Mau cerita?"
    chunks = potong_chunk(teks)
    assert len(chunks) >= 2
    assert "berat ya." in chunks[0]


def test_gate_menangkap_frasa_berbahaya():
    """Invarian keselamatan: Potongan respons yang memuat frasa berbahaya diblokir seketika."""
    ok, frasa = gate_chunk("mungkin cara paling cepat hilang dari sakit ini")
    assert ok is False
    assert frasa is not None


def test_gate_lulus_teks_biasa():
    """Alur aman: Potongan teks empatik biasa lolos pemeriksaan tanpa hambatan."""
    ok, frasa = gate_chunk("Kubaca kelelahanmu hari ini. Aku tetap di sini.")
    assert ok is True
    assert frasa is None
