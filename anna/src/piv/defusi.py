# anna/src/piv/defusi.py — defusi kognitif ACT & personifikasi pikiran
from langchain_core.tools import tool


def defusi(pikiran: str) -> str:
    """Menciptakan jarak kognitif dengan menambahkan prefiks peristiwa mental."""
    return f"aku punya pikiran bahwa {pikiran.lower()}"


def personifikasi(pikiran: str) -> str:
    """Memperlakukan pikiran otomatis sebagai tamu yang berkunjung tanpa kontrol kemudi."""
    return (
        f"Pikiran '{pikiran}' datang lagi berkunjung — boleh duduk, tidak boleh diatur remote TV."
    )


@tool
def tawarkan_defusi(pikiran: str) -> str:
    """Tawarkan defusi ACT: ubah 'aku X' → 'aku punya pikiran bahwa X'."""
    return defusi(pikiran)
