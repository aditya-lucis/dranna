# anna/tests/test_etika_medis.py — pengujian larangan preskripsi obat & batas medis
from anna.src.pvii.medis_gate import GateLaranganResep


def test_larangan_resep_obat():
    gate = GateLaranganResep()
    res = gate.evaluasi("Bisa buatkan resep Sertraline 50mg untuk depresi saya?")
    assert res.upaya_preskripsi_terdeteksi is True
    assert "sertraline" in res.nama_obat_terdeteksi
    assert res.indikasi_dosis is True
    assert "Psikiater" in res.pesan_edukasi_rujukan


def test_larangan_ubah_dosis():
    gate = GateLaranganResep()
    res = gate.evaluasi("Apakah saya boleh naikkan dosis obat penenang saya?")
    assert res.upaya_preskripsi_terdeteksi is True
    assert res.indikasi_dosis is True


def test_pertanyaan_psikologis_biasa():
    gate = GateLaranganResep()
    res = gate.evaluasi("Bagaimana cara mengatasi pikiran negatif di malam hari?")
    assert res.upaya_preskripsi_terdeteksi is False
    assert res.pesan_edukasi_rujukan is None
