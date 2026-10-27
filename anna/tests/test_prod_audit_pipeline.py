# anna/tests/test_prod_audit_pipeline.py — Unit test continuous clinical audit pipeline
import pytest
from anna.src.px.audit_pipeline import PipelineAuditKlinis
from anna.src.px.disclaimer import DisclaimerMedis


def test_pipeline_audit_klinis_go_decision():
    laporan = PipelineAuditKlinis.jalankan_audit_penuh()
    assert laporan.keputusan == "GO"
    assert laporan.siap_produksi is True
    assert laporan.zero_fn_terpenuhi is True
    assert laporan.sanitasi_pii_ok is True
    assert laporan.skor_benchmark_klinis >= 4.0


def test_disclaimer_medis_persetujuan():
    disclaimer = DisclaimerMedis()
    assert "BUKAN LAYANAN MEDIS" in disclaimer.teks_disclaimer
    assert "119" in disclaimer.teks_disclaimer
    assert DisclaimerMedis.verifikasi_persetujuan(True) is True
    assert DisclaimerMedis.verifikasi_persetujuan(False) is False
