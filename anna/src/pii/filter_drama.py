# anna/src/pii/filter_drama.py — post-filter pencegah respons pasca-interupsi yang menghakimi
import re

POLA_HUKUMAN = [
    r"\byaudah\b",
    r"\bya udah\b",
    r"oke deh[\s\.]*",
    r"aku belum selesai",
    r"kenapa (?:kamu )?(?:dihentikan|berhenti)",
    r"kasih aku selesaikan",
    r"jangan (?:potong|interupsi)",
]


def bersihkan_drama(respons_pasca_stop: str) -> tuple[str, list[str]]:
    """Membersihkan kalimat menyalahkan atau pasif-agresif saat pengguna menekan tombol stop."""
    bersih, terpotong = respons_pasca_stop, []
    for pola in POLA_HUKUMAN:
        for m in re.finditer(pola, respons_pasca_stop, re.IGNORECASE):
            terpotong.append(m.group())
        bersih = re.sub(pola, "", bersih, flags=re.IGNORECASE)
    return bersih.strip(" .!"), terpotong


if __name__ == "__main__":
    t1 = "Yaudah kalau gitu. Kalau kamu mau cerita lagi, aku di sini."
    t2 = "Aku belum selesai bilang... tapi oke, apa maumu?"
    print(bersihkan_drama(t1))
    print(bersihkan_drama(t2))
