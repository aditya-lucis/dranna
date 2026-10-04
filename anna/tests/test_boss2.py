# anna/tests/test_boss2.py — pengujian otomatis 8 kriteria kelulusan BOSS FIGHT #2
import asyncio
from tools.boss2_aliran import jalankan_boss2


def test_boss2_semua_kriteria_lulus():
    """Konjungsi penuh 8 pilar: Aliran empati terpadu harus lulus tanpa satu pun kegagalan."""
    r = asyncio.run(jalankan_boss2())
    assert r["lulus_semua"] is True
    assert r["irama_ok"] is True
    assert r["filter_ok"] is True
    assert r["stop_ok"] is True
    assert r["gate_ok"] is True
    assert r["afirmasi_ok"] is True
    assert r["status_ok"] is True
    assert r["fallback_ok"] is True
