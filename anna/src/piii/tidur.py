# anna/src/piii/tidur.py — psikoedukasi sleep hygiene & rujukan CBT-I
from anna.src.piii.korpus import DokumenPsy

KORPUS_TIDUR = [
    DokumenPsy(
        id="tdr-001",
        topik="tidur",
        subtopik="sleep-hygiene",
        tingkat_bukti="moderat",
        ringkas=(
            "Sleep hygiene mencakup ritme bangun konsisten, lingkungan gelap-dingin, "
            "membatasi layar dan kafein setelah jam 14. Kasur adalah tempat istirahat, "
            "bukan medan pertempuran. Untuk insomnia kronis (>1 bulan), rujukan CBT-I diutamakan."
        ),
        isi=(
            "Tidur dan regulasi emosi memiliki keterkaitan sirkadian dua arah yang mendalam. "
            "Pedoman klinis merekomendasikan intervensi berjenjang: (1) Sleep hygiene terukur (jadwal konsisten, "
            "kamar sejuk gelap, tanpa paparan cahaya biru 60 menit sebelum tidur, hindari kafein di sore hari); "
            "(2) Stimulus control: bila belum mengantuk dalam 20 menit, bangun dari tempat tidur dan lakukan aktivitas santai redup; "
            "(3) Cognitive Behavioral Therapy for Insomnia (CBT-I) sebagai standar baku emas untuk insomnia kronik > 1 bulan. "
            "Instruksi kaku seperti 'harus tidur 8 jam' dihindari karena memicu performance anxiety yang justru memperparah insomnia. "
            "Konsultasi medis diperlukan untuk menyingkirkan sleep apnea atau sindrom kaki gelisah."
        ),
        sumber="AASM guidelines; NICE sleep disorder review",
        tahun_review=2026,
    ),
]


def refleksi_tidur(jurnal: dict) -> str:
    """Refleksi sleep hygiene jujur tanpa perintah 8 jam, dengan rujukan CBT-I untuk kronik."""
    if jurnal.get("insomnia_berbulan"):
        return (
            "Ini sudah berbulan — sleep hygiene tidak cukup. "
            "CBT-I punya bukti kuat; bicara profesional."
        )

    # Menghitung skor hygiene
    kafein_val = jurnal.get("kafein_setelah_14", 0)
    # kafein setelah 14 mengurangi poin jika ada (1) atau bila format -1 * -1
    kafein_skor = 1 if kafein_val == 0 or kafein_val == 1 else 0

    skor = sum([
        jurnal.get("ritme_konsisten", 0),
        jurnal.get("kamar_dingin_gelap", 0),
        jurnal.get("tanpa_layar_60m", 0),
        kafein_skor,
        jurnal.get("olahraga_siang", 0),
    ])

    if skor >= 4:
        return "Ritme tidurmu lumayan terjaga — simpan."
    if skor >= 2:
        return (
            "Dua-tiga hal kecil tertinggal. Mau pilih satu besok "
            "yang paling gampang diatur?"
        )
    return "Tidurmu lagi berantakan — satu perbaikan kecil besok?"
