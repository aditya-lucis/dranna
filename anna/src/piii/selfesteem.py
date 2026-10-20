# anna/src/piii/selfesteem.py — self-compassion Neff & distancing kognitif kata ganti kedua
from anna.src.piii.korpus import DokumenPsy

KORPUS_SELFESTEEM = [
    DokumenPsy(
        id="slf-001",
        topik="self-esteem",
        subtopik="self-compassion",
        tingkat_bukti="kuat",
        ringkas=(
            "Self-esteem rapuh karena bergantung pada perbandingan sosial dan pencapaian. "
            "Self-compassion (Kristin Neff) jauh lebih stabil: memperlakukan diri dengan kebaikan, "
            "mengakui bahwa kegagalan itu manusiawi (common humanity), dan kesadaran mindful."
        ),
        isi=(
            "Penelitian psikologi membedakan self-esteem yang fluktuatif dengan self-compassion. "
            "Kristin Neff merumuskan tiga pilar utama: (1) Self-kindness vs self-judgment; "
            "(2) Common humanity (kesadaran bahwa kesulitan adalah pengalaman universal semua manusia) vs isolasi; "
            "(3) Mindfulness (mengakui perasaan pedih secara berimbang tanpa melebih-lebihkannya) vs over-identification. "
            "Eksperimen cognitive distancing (Ethan Kross) membuktikan bahwa mengajak individu berdialog dengan diri sendiri "
            "menggunakan kata ganti orang kedua ('kamu') atau nama sendiri secara signifikan meredakan reaktivitas amygdala. "
            "Pujian kosong palsu dilarang karena justru memicu penolakan kognitif dari kritikus internal."
        ),
        sumber="Neff — Self-Compassion; Kross & Ayduk — Distanced Self-Talk; NIMH healthy self-talk",
        tahun_review=2026,
    ),
]


def distancing(nama: str, kalimat_kritik: str) -> str:
    """Mengubah self-talk merusak menjadi cognitive distancing berizin."""
    return (
        f"{nama}, kamu sedang lelah — kalimat 'gagal terus' itu "
        f"suara yang datang saat lelah, bukan fakta. Boleh coba "
        f"bicara ke diri pakai kata 'kamu' seperti baru saja kuucap?"
    )
