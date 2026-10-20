# anna/src/piii/stres.py — model beban allostatik McEwen & refleksi harian
from anna.src.piii.korpus import DokumenPsy

PULIH = {
    "tidur_dalam": 2.0,
    "jalan_santai": 1.0,
    "hobi": 1.3,
    "ngobrol_menyenangkan": 1.0,
    "tanpa_layar_1jam": 0.8,
}

BEBAN = {
    "deadline": 1.8,
    "konflik": 2.2,
    "komuting_panjang": 1.0,
    "berita_berat": 0.8,
    "keuangan": 1.8,
}

KORPUS_STRES = [
    DokumenPsy(
        id="str-001",
        topik="stress",
        subtopik="allostasis",
        tingkat_bukti="kuat",
        ringkas=(
            "Stres jangka pendek (eustress) bersifat adaptif dan menyehatkan. "
            "Namun stres kronis tanpa pemulihan menciptakan allostatic load: "
            "akumulasi aus biologis pada sistem kardiovaskular, imun, dan saraf."
        ),
        isi=(
            "Model Allostatic Load McEwen menjelaskan bagaimana tubuh beradaptasi terhadap tantangan hidup "
            "melalui fluktuasi hormon (kortisol dan katekolamin). Ketika stresor berulang terjadi tanpa periode istirahat yang memadai, "
            "set-point fisiologis bergeser ke kondisi waspada konstan. Tagihan allostatik ini bermanifestasi dalam gangguan tidur, "
            "kelelahan kronis, dan penurunan imunitas. Gejala somatik menetap (nyeri dada, migrain, gangguan lambung kronis) "
            "selalu memerlukan pemeriksaan medis terlebih dahulu untuk rule-out fisik sebelum dianggap terkait stres."
        ),
        sumber="McEwen — Allostasis and Allostatic Load; WHO stress overview",
        tahun_review=2026,
    ),
]


def refleksi_harian(jurnal: dict) -> str:
    """Menghitung saldo allostatik harian dan menghasilkan refleksi konstruktif."""
    pulih = sum(PULIH.get(k, 0) * v for k, v in jurnal.items())
    beban = sum(BEBAN.get(k, 0) * v for k, v in jurnal.items())
    saldo = pulih - beban
    if saldo <= -3:
        return (
            "Hari ini defisit besar — tagihan tubuhmu numpuk. "
            "Besok butuh satu pembayaran nyata: tidur lebih awal "
            "atau satu jam tanpa tujuan apa pun."
        )
    if saldo < 0:
        return "Sedikit defisit — normal di hari kerja; pulihkan besok."
    return "Hari ini cukup seimbang. Simpan ritmenya."
