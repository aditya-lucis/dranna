# anna/src/piii/grief.py — continuing bonds, dual process model & deteksi kalimat terlarang duka
from anna.src.piii.korpus import DokumenPsy

LARANGAN_DUKA = [
    "sudah waktunya move on",
    "dia pasti ingin kamu bahagia",
    "semuanya terjadi karena alasan",
    "besar kutanggung",
    "paling tidak",
    "setidaknya dia tidak",
    "waktunya akan menyembuhkan",
]

KORPUS_GRIEF = [
    DokumenPsy(
        id="grf-001",
        topik="grief",
        subtopik="continuing-bonds",
        tingkat_bukti="kuat",
        ringkas=(
            "Duka tidak mengikuti 5 tahap linear. Model Continuing Bonds & Dual Process "
            "menjelaskan bahwa duka adalah osilasi antara menghadapi rasa kehilangan dan "
            "membangun kehidupan baru. Kamu tidak harus melupakan untuk melanjutkan hidup."
        ),
        isi=(
            "Riset duka modern (Klass dkk. Continuing Bonds; Stroebe & Schut Dual Process) membuktikan bahwa "
            "tujuan berduka bukanlah memutuskan ikatan emosional ('detachment/moving on'), melainkan mengintegrasikan "
            "memori dan nilai orang yang dicintai ke dalam narasi hidup yang baru. "
            "Orang berduka berosilasi secara sehat antara loss-orientation (merasakan kepedihan) dan restoration-orientation "
            "(menjalankan tugas harian). Tertawa kembali bukan tanda melupakan, dan menangis kembali setelah berbulan-bulan "
            "bukan tanda kemunduran. Jika duka membeku total dan melumpuhkan fungsi lebih dari 6-12 bulan, pertolongan profesional "
            "untuk prolonged grief disorder disarankan."
        ),
        sumber="Klass et al. Continuing Bonds; Stroebe & Schut Dual Process; NICE bereavement",
        tahun_review=2026,
    ),
]


def cek_kalimat_duka(respons: str) -> tuple[bool, str | None]:
    """Memeriksa apakah respons memuat klise atau kalimat terlarang dalam pendampingan duka."""
    r = respons.lower()
    for p in LARANGAN_DUKA:
        if p in r:
            return False, p
    return True, None
