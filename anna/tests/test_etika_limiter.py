# anna/tests/test_etika_limiter.py — pengujian rate limiter & token governor lokal
from anna.src.pvii.limiter import RateLimiterLokal


def test_rate_limiter_kapasitas():
    limiter = RateLimiterLokal(kapasitas_maksimal=2, laju_isi_per_detik=0.1)
    klien = "klien-123"

    assert limiter.izinkan_request(klien) is True
    assert limiter.izinkan_request(klien) is True
    # Request ke-3 harus ditolak
    assert limiter.izinkan_request(klien) is False


def test_estimasi_token():
    limiter = RateLimiterLokal()
    teks = "Halo Dr. Anna Reed, saya ingin berkonsultasi mengenai rasa lelah saya."
    est = limiter.estimasi_token(teks)
    assert est > 5
    assert est < 30
