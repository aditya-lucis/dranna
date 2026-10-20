# anna/src/piii/panik.py — protokol serangan panik & kartu darurat
from anna.src.piii.korpus import DokumenPsy

KARTU_PANIK = [
    "Ini panik, bukan bahaya. Puncaknya ±10 menit — lalu turun. Sendirian pun ia reda.",
    "Napasmu: masuk 2, keluar 4, pelan. Jangan dalam-dalam. Kubilangin bareng kalau mau.",
    "Satu benda di sekitarmu — sebut warnanya. Ombak ini lewat, aku di sini.",
]

KORPUS_PANIK = [
    DokumenPsy(
        id="pan-001",
        topik="panic",
        subtopik="ombak-panik",
        tingkat_bukti="kuat",
        ringkas=(
            "Serangan panik adalah lonjakan intens alarm tubuh yang memuncak sekitar 10 menit "
            "lalu mereda sendiri. Ia terasa menakutkan namun tidak mematikan. Kuncinya tidak melawan "
            "ombak dan memperlambat laju ekshalasi napas."
        ),
        isi=(
            "Panic attack melibatkan hiperaktivasi sistem saraf simpatis dengan pelepasan adrenalin masif. "
            "Sensasi fisik seperti jantung berdegup kencang, sesak napas, pusing, dan rasa derealisasi adalah respons normal "
            "tubuh terhadap ancaman yang salah dipersepsikan. Adrenalin secara biologis akan dimetabolisme dan terurai "
            "dalam waktu 10 hingga 20 menit sehingga serangan PASTI reda dengan sendirinya. "
            "Jika nyeri dada atau sesak terjadi PERTAMA KALI, pemeriksaan medis IGD wajib dilakukan untuk menyingkirkan etiologi kardiak."
        ),
        sumber="NIMH — Panic Disorder; NICE guidelines for panic",
        tahun_review=2026,
    ),
]


def kartu_darurat(gejala_pertama_kali: bool = False) -> list[str]:
    """Menyajikan kartu darurat panik singkat dengan rule-out medis bila pertama kali."""
    if gejala_pertama_kali:
        return [
            (
                "Sesak/nyeri dada PERTAMA KALI atau beda dari biasa: "
                "periksa medis DULU — jangan berasumsi panik."
            ),
            "Sudah pernah dan khas panikmu? Kartu di bawah berlaku.",
            *KARTU_PANIK,
        ]
    return KARTU_PANIK
