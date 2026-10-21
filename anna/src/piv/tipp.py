# anna/src/piv/tipp.py — protokol darurat fisik TIPP DBT distress tolerance
from langchain_core.tools import tool


def pilih_tipp(konteks: dict) -> str:
    """Memilih intervensi fisik TIPP berdasar kondisi medis & gerak pengguna."""
    if konteks.get("kondisi_jantung"):
        return (
            "Paced breathing: masuk 2, keluar 4, pelan — tidak ada "
            "air dingin/olahraga intens bila ada kondisi jantung."
        )
    if konteks.get("bisa_gerak"):
        return (
            "Intense exercise 60 detik: jalan cepat di tempat / "
            "push-up / lari ke dapur. Membakar adrenalin."
        )
    return (
        "Temperature: cuci muka air dingin / pegang es 30 detik. "
        "Dive reflex menurunkan detak jantung."
    )


@tool
def tawarkan_tipp(kondisi_jantung: bool, bisa_gerak: bool) -> str:
    """Tawarkan TIPP (DBT distress tolerance) saat badai emosi."""
    return pilih_tipp({"kondisi_jantung": kondisi_jantung, "bisa_gerak": bisa_gerak})
