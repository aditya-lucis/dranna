# anna/src/piv/values.py — Values Compass ACT 8 domain & komitmen tindakan kecil
from langchain_core.tools import tool

DOMAIN = [
    "keluarga",
    "intim",
    "teman",
    "kerja",
    "pendidikan",
    "rekreasi",
    "kewargaan",
    "spiritualitas",
]


def prompt_nilai(domain: str) -> str:
    """Menghasilkan prompt nilai hidup terfokus pada dorongan autentik internal."""
    return (
        f"Dalam domain {domain}, apa yang sungguh penting bagimu — "
        f"bukan apa yang orang lain mau, bukan apa yang nyaman? "
        f"Satu kalimat."
    )


def tindakan_kecil(nilai: str) -> str:
    """Mengajak komitmen mikro yang menoleransi ketidaknyamanan tanpa membahayakan."""
    return (
        "Satu tindakan kecil minggu ini ke arah itu — yang sanggup "
        "kamu lakukan meski tidak nyaman?"
    )


@tool
def mulai_values_compass() -> str:
    """Pilih satu domain kehidupan, identifikasi nilai, satu tindakan kecil."""
    return "Domain: " + ", ".join(DOMAIN[:4]) + " — mana yang paling terpanggil hari ini?"
