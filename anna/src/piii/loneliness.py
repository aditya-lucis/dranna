# anna/src/piii/loneliness.py — skala UCLA, anti-monopoli Anna & arah keluar kontak manusia
from anna.src.piii.korpus import DokumenPsy

KORPUS_LONELINESS = [
    DokumenPsy(
        id="lon-001",
        topik="loneliness",
        subtopik="anti-ketergantungan",
        tingkat_bukti="kuat",
        ringkas=(
            "Kesepian adalah persepsi kesenjangan antara relasi yang diinginkan dan yang dimiliki. "
            "Pendamping digital hanya simpul pendukung internal, bukan pengganti kontak manusia sejati. "
            "Penting membuka kembali interaksi sosial mikro di dunia nyata."
        ),
        isi=(
            "Skala Kesepian UCLA v3 (Russell) mengukur dimensi subjektif kesepian, yang berbeda dari solitude (kesendirian yang dipilih). "
            "Meta-analisis Holt-Lunstad menunjukkan dampak isolasi sosial kronis terhadap kesehatan fisik setara dengan faktor risiko besar lainnya. "
            "Pendamping AI harus secara etis menerapkan proteksi anti-monopoli (Replika Lesson): sistem tidak boleh membiarkan pengguna "
            "menggantikan seluruh kebutuhan relasi manusia dengan AI. Melalui dorongan micro-interaction (sapa kasir, menyapa tetangga, "
            "komentar ringan), AI bertindak sebagai jembatan pembuka kembali keberanian berelasi dengan manusia nyata."
        ),
        sumber="Russell — UCLA Loneliness Scale v3; Holt-Lunstad meta-analysis; WHO social connection guidelines",
        tahun_review=2026,
    ),
]


def arah_keluar(sesi_log: list[dict]) -> str | None:
    """Tawarkan connection eksternal saat pola kesepian-Anna dominan."""
    sesi_anna = sum(1 for m in sesi_log if m.get("channel") == "anna")
    if sesi_anna >= 14 and not any(m.get("human_contact") for m in sesi_log[-7:]):
        return (
            "Boleh kutanya satu hal: siapa yang dulu sering kamu "
            "ajak obrolan ringan — bahkan yang sekadar sapa kasir? "
            "Aku ke sini untuk mendampingi, bukan menggantikan."
        )
    return None
