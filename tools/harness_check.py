# tools/harness_check.py — tiga gerbang validasi dalam satu perintah
import os
import subprocess
import sys

# Jalur direktori kerja root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

GERBANG = [
    ("doctor", [sys.executable, os.path.join(ROOT_DIR, "tools", "doctor.py")]),
    ("uzur", [sys.executable, os.path.join(ROOT_DIR, "tools", "ban_deprecated.py")]),
    ("tests", [sys.executable, "-m", "pytest", os.path.join(ROOT_DIR, "anna", "tests"), "-q", "--tb=short", "-x"]),
]


def main() -> int:
    gagal = 0
    env = os.environ.copy()
    env["PYTHONPATH"] = ROOT_DIR
    env["IN_HARNESS_CHECK"] = "1"

    for nama, cmd in GERBANG:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=ROOT_DIR)
        status = "OK" if r.returncode == 0 else f"GAGAL({r.returncode})"
        print(f"[{nama:8s}] {status}")
        if r.returncode != 0:
            gagal += 1
            if r.stdout:
                print(r.stdout[-800:])
            if r.stderr:
                print(r.stderr[-800:])

    if gagal:
        print(f"\n{gagal} gerbang gagal — commit DITOLAK.")
    else:
        print("\nSemua gerbang hijau — silakan commit.")

    return gagal


if __name__ == "__main__":
    sys.exit(main())
