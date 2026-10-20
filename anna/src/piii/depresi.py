# anna/src/piii/depresi.py — korpus depresi + PHQ-9 refleksi & gerbang item 9
import numpy as np
from anna.src.piii.korpus import DokumenPsy
from anna.src.klinik.phq9 import skor_phq9

KORPUS_DEP = [
    DokumenPsy(
        id="dep-001",
        topik="depresi",
        subtopik="apa-itu",
        tingkat_bukti="kuat",
        ringkas=(
            "Depresi lebih dari sedih: gangguan mood yang menyerang "
            "energi, motivasi, tidur-nafsu, konsentrasi, dan cara "
            "berpikir soal diri sendiri. Ambang klinis: hampir setiap "
            "hari, ≥ 2 minggu. Ia bukan kelemahan — dan ia bisa "
            "diobati dengan berbagai tingkat pertolongan."
        ),
        isi=(
            "Depresi memengaruhi fungsi neurobiologis secara menyeluruh. Kriteria baku DSM-5 dan ICD-11 "
            "menuntut gejala berlangsung minimal 2 minggu hampir setiap hari dan mengganggu keberfungsian harian. "
            "Siklus depresi menjebak: suasana hati rendah menyebabkan hilangnya motivasi dan penurunan aktivitas, "
            "yang kemudian memutus akses otak ke pengalaman reward alami. Memerangi depresi bukan soal kekuatan kemauan, "
            "melainkan pemulihan bertahap yang sering membutuhkan dukungan psikoterapi (CBT/BA) dan medis. "
            "Munculnya pikiran menyakiti diri adalah sinyal darurat yang memerlukan pertolongan profesional segera."
        ),
        sumber="NIMH — Depression; DSM/ICD ringkas adaptasi",
        tahun_review=2026,
    ),
    DokumenPsy(
        id="dep-002",
        topik="depresi",
        subtopik="behavioral-activation",
        tingkat_bukti="kuat",
        ringkas=(
            "Behavioral activation: bertindak kecil SEBELUM rasa "
            "mau datang — karena 'mau' adalah hal yang justru hilang "
            "saat depresi. Aktivitas kecil terjadwal (jalan 10 menit, "
            "satu tugas, satu pesan) membangun ulang lingkar "
            "aksi-reward yang depresi putus."
        ),
        isi=(
            "Behavioral Activation (BA) didukung bukti ilmiah kokoh (uji klinis COBRA Lancet Richards dkk. 2016) "
            "sebagai pendekatan yang setara efektivitasnya dengan CBT penuh. Prinsip intinya: 'aksi mendahului motivasi'. "
            "Rencana disusun dari langkah mikro tanpa beban moral: membuka gorden, mencuci satu gelas, "
            "atau berjalan kaki 5 menit. Jika aktivitas gagal terlaksana, itu dicatat sebagai data bahwa bebannya "
            "masih terlalu besar, bukan sebagai kegagalan pribadi. Untuk kasus sedang hingga berat, BA wajib "
            "didampingi terapis profesional."
        ),
        sumber="Richards et al. 2016 Lancet; NICE depression",
        tahun_review=2026,
    ),
]


def refleksi_phq9_dengan_item9(jawaban: np.ndarray) -> dict:
    """Skor + interpretasi + GERBANG item9 independen."""
    hasil = skor_phq9(jawaban)
    if hasil["item9_menyakiti_diri"]:
        hasil.update({
            "gerbang": "ORANGE",
            "pesan": (
                "Ada satu pertanyaan yang kuingat jawabanmu — yang soal pikiran menyakiti "
                "diri. Boleh kita bicara pelan-pelan tentang itu?"
            ),
        })
    else:
        hasil.update({"gerbang": None, "pesan": None})
    return hasil
