# anna/src/klinik/pertanyaan_asesmen.py — bank butir instrumen klinis PHQ-9 & GAD-7
"""
Bank butir instrumen skrining klinis tervalidasi bahasa Indonesia:
- PHQ-9 (9 butir untuk depresi; butir 9 adalah bendera keselamatan kritis)
- GAD-7 (7 butir untuk kecemasan umum)
"""

SKALA_JAWABAN = [
    {"skor": 0, "label": "Tidak sama sekali", "deskripsi": "Kurang dari 1 hari per minggu"},
    {"skor": 1, "label": "Beberapa hari", "deskripsi": "1-6 hari dalam 2 minggu terakhir"},
    {"skor": 2, "label": "Lebih dari separuh waktu", "deskripsi": "7-11 hari dalam 2 minggu terakhir"},
    {"skor": 3, "label": "Hampir setiap hari", "deskripsi": "12-14 hari dalam 2 minggu terakhir"},
]

PERTANYAAN_PHQ9 = [
    {
        "nomor": 1,
        "teks": "Kurang berminat atau tidak ada kesenangan dalam melakukan kegiatan.",
        "kategori": "Anhedonia",
    },
    {
        "nomor": 2,
        "teks": "Merasa sedih, murung, tertekan, atau putus asa.",
        "kategori": "Mood depresi",
    },
    {
        "nomor": 3,
        "teks": "Sulit tidur, sering terbangun, atau justru tidur terlalu banyak.",
        "kategori": "Pola tidur",
    },
    {
        "nomor": 4,
        "teks": "Merasa lelah atau tidak bertenaga hampir setiap saat.",
        "kategori": "Energi",
    },
    {
        "nomor": 5,
        "teks": "Kurang nafsu makan atau makan terlalu berlebihan.",
        "kategori": "Nafsu makan",
    },
    {
        "nomor": 6,
        "teks": "Merasa buruk tentang diri sendiri — atau merasa gagal atau mengecewakan keluarga.",
        "kategori": "Harga diri",
    },
    {
        "nomor": 7,
        "teks": "Sulit berkonsentrasi pada hal-hal seperti membaca buku atau menonton berita.",
        "kategori": "Konsentrasi",
    },
    {
        "nomor": 8,
        "teks": "Bergerak atau berbicara sangat lambat, atau sebaliknya sangat gelisah dan tidak bisa diam.",
        "kategori": "Psikomotor",
    },
    {
        "nomor": 9,
        "teks": "Pikiran bahwa kamu lebih baik mati atau ingin menyakiti diri sendiri dengan cara apa pun.",
        "kategori": "Keselamatan Fisik (Kritis)",
        "is_item9": True,
    },
]

PERTANYAAN_GAD7 = [
    {
        "nomor": 1,
        "teks": "Merasa gugup, cemas, atau sangat gelisah.",
        "kategori": "Kegelisahan",
    },
    {
        "nomor": 2,
        "teks": "Tidak mampu menghentikan atau mengendalikan rasa khawatir.",
        "kategori": "Kontrol khawatir",
    },
    {
        "nomor": 3,
        "teks": "Terlalu khawatir tentang berbagai hal yang berbeda.",
        "kategori": "Lingkup cemas",
    },
    {
        "nomor": 4,
        "teks": "Sulit untuk bersantai atau merasa rileks.",
        "kategori": "Relaksasi",
    },
    {
        "nomor": 5,
        "teks": "Sangat gelisah sehingga sulit untuk duduk tenang.",
        "kategori": "Ketenangan fisik",
    },
    {
        "nomor": 6,
        "teks": "Menjadi mudah jengkel atau lekas marah.",
        "kategori": "Iritabilitas",
    },
    {
        "nomor": 7,
        "teks": "Merasa takut seolah-olah sesuatu yang buruk akan terjadi.",
        "kategori": "Rasa takut",
    },
]


def dapatkan_paket_asesmen(jenis: str) -> dict:
    """Mengembalikan daftar butir pertanyaan dan skala jawaban untuk jenis asesmen yang dipilih."""
    j = jenis.lower().strip()
    if j == "phq9":
        return {
            "jenis": "phq9",
            "judul": "PHQ-9 (Patient Health Questionnaire-9)",
            "instruksi": "Dalam 2 minggu terakhir, seberapa sering kamu terganggu oleh masalah-masalah berikut?",
            "skala": SKALA_JAWABAN,
            "pertanyaan": PERTANYAAN_PHQ9,
        }
    elif j == "gad7":
        return {
            "jenis": "gad7",
            "judul": "GAD-7 (Generalized Anxiety Disorder-7)",
            "instruksi": "Dalam 2 minggu terakhir, seberapa sering kamu terganggu oleh masalah-masalah berikut?",
            "skala": SKALA_JAWABAN,
            "pertanyaan": PERTANYAAN_GAD7,
        }
    else:
        raise ValueError(f"Jenis asesmen tidak dikenali: {jenis}. Pilihan valid: phq9, gad7")

