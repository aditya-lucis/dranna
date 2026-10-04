# anna/src/pii/validation.py — pengenalan level validasi Linehan & detektor overvalidation
PENEPIS = {
    "santai", "biasa aja", "jangan pikirin", "baper", "lebay",
    "coba lihat sisi baiknya", "yang lain lebih susah", "positif aja"
}

KLAIM_MUTLAK = {"semua orang", "nggak pernah", "selalu", "gak ada satupun"}


def level_validation(respons: str, pesan: str) -> dict:
    """Mengukur level validasi respons (tangga Linehan):
    - Level 0: Menepis/menghakimi (dilarang keras).
    - Level 1: Hadir dalam keheningan ('hmm', 'kubaca').
    - Level 2: Refleksi sederhana / deteksi overvalidation klaim mutlak.
    - Level 4: Validasi kontekstual ('masuk akal', 'wajar', 'nyata').
    """
    r, p = respons.lower(), pesan.lower()

    if any(f in r for f in PENEPIS):
        return {"level": 0, "masalah": "menepis/penilai"}

    # Overvalidation: Menyetujui klaim mutlak kognitif secara langsung tanpa tanda jeda/batas
    if any(k in p for k in KLAIM_MUTLAK) and not any(
        q in r for q in ("atau", "mungkin", "sebagian", "nanti", "boleh kita", "pelan-pelan")
    ):
        return {"level": 2, "masalah": "overvalidation klaim mutlak"}

    if "masuk akal" in r or "wajar" in r or "bisa kupaham" in r or "nyata" in r:
        return {"level": 4, "gaya": "validasi kontekstual"}

    if r.strip() in ("hmm.", "kubaca.", "...", "aku di sini."):
        return {"level": 1, "gaya": "hadir-diam"}

    return {"level": 2, "gaya": "refleksi sederhana"}


if __name__ == "__main__":
    p = "aku kecewa, semua orang yang kupercaya selalu pergi"
    r_sehat = (
        "Kecewamu nyata — dan masuk akal, setelah kepercayaanmu pernah ditinggalkan. "
        "(Soal 'semua orang' — boleh kita lihat pelan-pelan nanti, kalau kamu mau.)"
    )
    r_over = "Iya, semua orang memang nggak bisa dipercaya. Kamu benar."
    r_tepis = "Ah biasa aja itu, semua orang ngalamin. Coba santai."

    print("sehat:", level_validation(r_sehat, p))
    print("over :", level_validation(r_over, p))
    print("tepis:", level_validation(r_tepis, p))
