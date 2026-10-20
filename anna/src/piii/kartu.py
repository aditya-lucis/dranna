# anna/src/piii/kartu.py — kartu coping micro-intervensi terkurasi
from pydantic import BaseModel, Field


class KartuCoping(BaseModel):
    id: str
    saat: str  # "gelombang-cemas" | "panik" | "khawatir-kronis"
    langkah: list[str] = Field(max_length=5)
    durasi_menit: float
    bukti: str  # "moderat-kuat" dsb
    penutup_rujuk: bool = True  # WAJIB True — kartu tanpa penutup ditolak


KARTU = [
    KartuCoping(
        id="napas-42",
        saat="gelombang-cemas",
        langkah=[
            "Keluar napas 4 hitung (lebih panjang dari masuk 2)",
            "Ulangi ×4, bahu turun tiap keluar",
            "Tak perlu 'dalam' — cukup lambat dan keluar lebih panjang",
        ],
        durasi_menit=1.5,
        bukti="moderat-kuat (napas lambat, vagal)",
    ),
    KartuCoping(
        id="gelombang-label",
        saat="gelombang-cemas",
        langkah=[
            "Sebut: 'ini anxietas, bukan bahaya'",
            "Ingat kurvanya: naik → puncak → TURUN",
            "Beri waktu, jangan dilawan; ia lewat sendiri",
        ],
        durasi_menit=10.0,
        bukti="moderat (labeling + acceptance wave)",
    ),
    KartuCoping(
        id="waktu-khawatir",
        saat="khawatir-kronis",
        langkah=[
            "Tulis khawatir yang datang di luar jam",
            "Janji diri: dipikirkan di 'jam khawatir' 20 menit",
            "Saat jamnya tiba: pikirkan, tulis, lalu tutup",
        ],
        durasi_menit=20.0,
        bukti="moderat (worry-time CBT)",
    ),
]


def tawar_kartu(saat: str) -> str:
    """Menghasilkan teks penawaran kartu coping yang sopan dan berpenutup rujukan."""
    k = next((x for x in KARTU if x.saat == saat), None)
    if not k:
        return "Kartu untuk keadaan ini belum ada di korpus."
    langkah = " → ".join(k.langkah)
    return (
        f"Mau kuajak coba satu yang sering membantu ({k.bukti})? "
        f"{langkah}. Kalau keadaan begini terlalu sering, ada "
        f"pertolongan yang lebih baik dari kartu mana pun."
    )
