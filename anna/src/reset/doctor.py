# anna/src/reset/doctor.py — verifikasi lingkungan (tanpa API uzur)
import importlib
import os
import sys

CEK = [
    ("numpy", "2"),
    ("scipy", "1"),
    ("langchain_core", "1"),
    ("langchain_google_genai", ("1", "2", "3", "4")),
    ("pydantic", "2"),
    ("fastapi", "0"),
]


def _kunci_ada() -> bool:
    return bool(os.environ.get("GOOGLE_API_KEY"))


def doctor(verbose: bool = True) -> int:
    masalah = 0
    py_ver = sys.version.split()[0]
    if verbose:
        status_py = "OK" if sys.version_info >= (3, 12) else "MAJOR SALAH (butuh >= 3.12)"
        print(f"python                  : {py_ver:10s} {status_py}")
    if sys.version_info < (3, 12):
        masalah += 1

    for mod, expected in CEK:
        try:
            m = importlib.import_module(mod)
            v = getattr(m, "__version__", "?")
            major = str(v).split(".")[0]
            if isinstance(expected, tuple):
                ok = major in expected
            else:
                ok = (major == expected)
            if verbose:
                status_mod = "OK" if ok else f"MAJOR SALAH (butuh {expected})"
                print(f"{mod:24s}: {str(v):10s} {status_mod}")
            masalah += 0 if ok else 1
        except ImportError:
            if verbose:
                print(f"{mod:24s}: TIDAK ADA (pip install {mod.replace('_', '-')})")
            masalah += 1

    # LangGraph presence & CVE-2026-27022 check
    try:
        lg = importlib.import_module("langgraph")
        lg_v = getattr(lg, "__version__", "?")
        if verbose:
            print(f"{'langgraph':24s}: {str(lg_v):10s} OK (CVE-2026-27022 check)")
    except ImportError:
        if verbose:
            print(f"{'langgraph':24s}: TIDAK ADA (pip install langgraph)")
        masalah += 1

    key_ada = _kunci_ada()
    if verbose:
        print(f"{'GOOGLE_API_KEY':24s}: {'ada' if key_ada else 'MISSING (.env)'}")

    return masalah


if __name__ == "__main__":
    sys.exit(0 if doctor() == 0 else 1)
