# anna/src/piv/distorsi.py — detektor 10 distorsi kognitif Burns/Beck sebagai hipotesis terbuka
import re

POLA = {
    "all_or_nothing": r"\b(selalu|tidak pernah|semua|tidak ada satupun)\b",
    "should": r"\b(harus(?:nya)?|seharusnya|wajib)\b",
    "catastrophizing": r"\b(pasti gagal|bencana|akhir|tidak akan pernah)\b",
    "labeling": r"\b(aku (?:bodoh|gagal|lemah|hina))\b",
}


def deteksi(pesan: str) -> list[str]:
    """Mendeteksi pola distorsi kognitif berbasis ekspresi reguler."""
    p = pesan.lower()
    return [k for k, pat in POLA.items() if re.search(pat, p)]


def tawar_distorsi(pesan: str) -> str | None:
    """Menawarkan hipotesis distorsi secara sopan dan berpintu keluar."""
    d = deteksi(pesan)
    if not d:
        return None
    nama = {
        "all_or_nothing": "pikiran hitam-putih (selalu/tidak pernah)",
        "should": "perkataan 'harus' yang menekan",
        "catastrophizing": "pikiran bencana",
        "labeling": "label diri yang keras",
    }
    dist_nama = nama.get(d[0], "pola pikiran otomatis")
    return f"Terdengar seperti {dist_nama} — boleh kita lihat apakah 100% benar?"
