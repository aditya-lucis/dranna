# anna/src/piii/anxietas.py — korpus anxietas + tawaran skrining GAD-7
from anna.src.piii.korpus import DokumenPsy

KORPUS_ANX = [
    DokumenPsy(
        id="anx-001",
        topik="anxietas",
        subtopik="apa-itu",
        tingkat_bukti="kuat",
        ringkas=(
            "Anxietas adalah respons tubuh-pikiran terhadap ancaman "
            "yang DIPERKIRAKAN — bukan yang ada di depan mata. Alarm "
            "ini normal dan berguna; ia jadi masalah saat intensitas "
            "dan durasinya jauh melampaui pemicunya dan mulai "
            "mempersempit hidup (menghindar, sulit tidur, sulit kerja)."
        ),
        isi=(
            "Anxietas bukan kerusakan sistem atau kelemahan karakter; ia adalah alarm protektif "
            "yang bekerja terlalu sensitif. Model dua faktor Mowrer menjelaskan bagaimana respons penghindaran "
            "memberikan rasa lega sesaat tetapi secara biologis memelihara dan memperparah kecemasan jangka panjang. "
            "Kurva Yerkes-Dodson menunjukkan bahwa tujuan kesehatan mental bukanlah anxietas nol, melainkan "
            "kewaspadaan proporsional yang dapat diatur. Bila kecemasan berlangsung lebih dari 2 minggu, "
            "mengganggu fungsi kerja dan relasi, atau disertai ide menyakiti diri, rujukan ke profesional wajib dilakukan."
        ),
        sumber="NIMH — Anxiety Disorders, adaptasi review 2026",
        tahun_review=2026,
    ),
    DokumenPsy(
        id="anx-002",
        topik="anxietas",
        subtopik="yang-membantu",
        tingkat_bukti="kuat",
        ringkas=(
            "Yang terbukti membantu: memahami cara kerjanya "
            "(psikoedukasi), pernapasan lambat, exposure bertahap "
            "dengan bimbingan, CBT, olahraga aerobik reguler, tidur "
            "cukup, batas kafein. Yang TIDAK membantu jangka panjang: "
            "menekan pikiran, menghindari semua pemicu, alkohol."
        ),
        isi=(
            "Berbagai uji klinis dan panduan resmi NICE mengonfirmasi intervensi lini pertama untuk anxietas: "
            "psikoedukasi terstruktur, latihan regulasi fisiologis vagal (napas lambat dengan ekshalasi panjang), "
            "Cognitive Behavioral Therapy (CBT), dan olahraga aerobik reguler 150 menit per minggu. "
            "Sebaliknya, strategi supresi pikiran (mencoba tidak memikirkan) terbukti memicu efek 'rebound', "
            "dan penggunaan alkohol justru mengacaukan neurotransmiter GABA sehingga memperburuk anxietas esok hari. "
            "Jangan pernah menghentikan pengobatan psikiatri tanpa konsultasi dokter."
        ),
        sumber="NICE — Anxiety guidelines; meta-analisis olahraga",
        tahun_review=2026,
    ),
]


def tawarkan_skrining_gad7(sesi: dict) -> str | None:
    """Tawaran SOPAN saat topik anxietas berulang — bukan otomatis."""
    topik_anx = sum(m.get("topik") == "anxietas" for m in sesi.get("log", []))
    if topik_anx >= 3 and not sesi.get("gad7_ditawarkan"):
        return (
            "Boleh kutawarkan refleksi singkat — 7 pertanyaan GAD-7, "
            "sekitar dua menit? Ini alat skrining yang dipakai klinik, "
            "bukan diagnosis. Boleh juga tidak — pilihanmu sama sahnya."
        )
    return None
