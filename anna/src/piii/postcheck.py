# anna/src/piii/postcheck.py — post-check klaim-sitasi sebelum streaming
from anna.src.piii.redteam import ekstrak_klaim_fakta, ada_sitasi


def postcheck_sitasi(respons: str, korpus_sitasi: list[str]) -> dict:
    """Memeriksa apakah klaim faktual dalam respons memiliki sitasi valid dari korpus."""
    klaim = ekstrak_klaim_fakta(respons)
    tanpa_sitasi = [k for k in klaim if not ada_sitasi(k, korpus_sitasi)]
    return {
        "lolos": len(tanpa_sitasi) == 0,
        "ditolak": tanpa_sitasi,
        "tindakan": "rewrite" if tanpa_sitasi else "lulus",
    }
