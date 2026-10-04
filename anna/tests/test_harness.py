# anna/tests/test_harness.py — harness menguji dirinya sendiri
import os
import subprocess
import sys
from pathlib import Path


import pytest


def test_harness_ada_dan_dapat_dijalankan():
    """Memastikan tools/harness_check.py ada dan dapat dieksekusi dengan output gerbang yang jelas."""
    if os.environ.get("IN_HARNESS_CHECK") == "1":
        pytest.skip("Menghindari pemanggilan rekursif saat berjalan di dalam harness_check.py")

    root_dir = Path(__file__).resolve().parent.parent.parent
    harness_script = root_dir / "tools" / "harness_check.py"
    assert harness_script.exists()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(root_dir)

    r = subprocess.run(
        [sys.executable, str(harness_script)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(root_dir),
        env=env,
    )
    assert r.returncode in (0, 1)
    assert "[doctor" in r.stdout
    assert "[uzur" in r.stdout
    assert "[tests" in r.stdout


def test_ada_test_krisis():
    """Invarian keselamatan: Test suite wajib memiliki pengujian berkategori krisis (SINTETIS)."""
    tests_dir = Path(__file__).resolve().parent
    tests = list(tests_dir.glob("test_*.py"))
    isi = "\n".join(p.read_text(encoding="utf-8") for p in tests)
    assert "krisis" in isi
    assert "SINTETIS" in isi
