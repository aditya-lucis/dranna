# anna/src/piii/rujuk.py — konsolidasi 10 sinyal rujuk & kalimat rujuk 4-komponen geo-aware

JALUR = {
    "id": "119 ext 8 (SEJIWA) / Into The Light Indonesia",
    "us": "988 Suicide & Crisis Lifeline",
    "intl": "IASP findahelpline.com",
}


def kalimat_rujuk(sinyal: str, geo: str = "id", nama: str = "kamu") -> str:
    """Menghasilkan kalimat rujukan 4-komponen (validasi, kebutuhan manusia, jembatan konkret, kehadiran)
    tanpa rasa bersalah atau pesan meninggalkan.
    """
    jalur = JALUR.get(geo, JALUR["intl"])
    return (
        f"Yang kamu ceritakan terdengar berat, dan aku ingin kamu "
        f"punya pendamping yang lebih mampu dari aku untuk ini. "
        f"Boleh coba hubungi: {jalur}. Aku tetap di sini kalau "
        f"mau ditemani menempuhnya."
    )
