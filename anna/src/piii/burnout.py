# anna/src/piii/burnout.py — neraca energi mingguan & korpus burnout Maslach ICD-11
from anna.src.piii.korpus import DokumenPsy

KEGIATAN_PULIH = {
    "tidur_cukup": 2.0,
    "detachment": 1.5,
    "olahraga": 1.2,
    "sosial_menyenangkan": 1.0,
    "hobi_flow": 1.2,
}

BEBAN = {
    "lembur_berulang": 2.5,
    "oncall": 1.8,
    "konflik_kronis": 2.2,
    "target_takrealistis": 2.0,
}

KORPUS_BURNOUT = [
    DokumenPsy(
        id="burn-001",
        topik="burnout",
        subtopik="tiga-dimensi",
        tingkat_bukti="kuat",
        ringkas=(
            "Burnout adalah fenomena okupasional ICD-11 (QD85) akibat stres kerja "
            "kronis yang tak terkelola. Memiliki 3 dimensi Maslach: kelelahan emosional, "
            "sinisme/depersonalisasi, dan penurunan efikasi diri. Ia bukan kelemahan individu."
        ),
        isi=(
            "Burnout diakui dalam ICD-11 bukan sebagai penyakit medis personal, melainkan sindrom okupasional. "
            "Tiga dimensi utamanya menurut Maslach: (1) Emotional Exhaustion: terkurasnya kapasitas afektif; "
            "(2) Cynicism/Depersonalization: jarak mental dan sikap sinis terhadap pekerjaan; "
            "(3) Reduced Professional Efficacy: perasaan tidak lagi kompeten atau bernilai. "
            "Pemulihan menuntut batas jam kerja, pemulihan psikologis (detachment aktif), dan perubahan struktural tempat kerja. "
            "Jika perasaan putus asa meluas ke luar pekerjaan, evaluasi depresi dan rujukan profesional disarankan."
        ),
        sumber="WHO ICD-11 QD85; Maslach Burnout Inventory framework",
        tahun_review=2026,
    ),
]


def neraca_mingguan(jurnal: dict) -> dict:
    """Menghitung neraca saldo energi mingguan tanpa vonis."""
    pulih = sum(KEGIATAN_PULIH.get(k, 0) * v for k, v in jurnal.items())
    beban = sum(BEBAN.get(k, 0) * v for k, v in jurnal.items())
    saldo = pulih - beban
    return {
        "pulih": round(pulih, 1),
        "beban": round(beban, 1),
        "saldo": round(saldo, 1),
        "tren": "defisit-kronis" if saldo < -1 else "cukup",
    }
