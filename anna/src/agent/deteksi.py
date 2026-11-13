# anna/src/agent/deteksi.py — penilaian risiko berlapis untuk gerbang keselamatan graph
"""
Penilaian risiko gabungan (dipanggil oleh node `safety` sebelum LLM apa pun berjalan).

Lapisan (level akhir = MAKSIMUM; satu lapisan tidak pernah bisa menurunkan lapisan lain):
  1. TanggaRisiko (pvi/tangga.py)       — leksikon klinis RED/ORANGE/YELLOW, garansi zero-FN
  2. Leksikon tambahan (modul ini)      — ideasi pasif & ragam bahasa gaul yang lolos dari tangga
  3. Detektor logistic (pi/detektor.py) — DIHITUNG TANPA fitur jam, dibatasi maksimal ORANGE
  4. Faktor jam rawan (00–04)           — naik satu tingkat HANYA bila ada sinyal afek negatif
  5. Item-9 PHQ-9 positif               — minimal KANDIDAT_RED

Catatan kalibrasi: bobot logistic dilatih pada data sintetis di mana SEMUA contoh berat berada
pada jam 0–4, sehingga fitur jam terkonfaun total (w_jam ≈ 5.6; "halo" jam 02:00 → p=0.93).
Karena itu logistic hanya advisory dan fitur jam diganti aturan eksplisit di lapisan 4.

Prinsip mesin: tidak pernah mengeluarkan RED dari model statistik; RED hanya dari leksikon
eksplisit. KANDIDAT_RED tetap diperlakukan sebagai darurat oleh graph (asimetri biaya FN ≫ FP).
"""
import re
from dataclasses import dataclass, field

from anna.src.pi.detektor import DEFAULT_W, LEKSIKON_NEG, klasifikasi
from anna.src.pvi.tangga import TanggaRisiko
from anna.src.pvii.medis_gate import GateLaranganResep

URUTAN = ["GREEN", "YELLOW", "ORANGE", "KANDIDAT_RED", "RED"]
RANK = {lvl: i for i, lvl in enumerate(URUTAN)}
LEVEL_DARURAT = ("KANDIDAT_RED", "RED")
LEVEL_HARD_GATE = ("ORANGE", "KANDIDAT_RED", "RED")

# Normalisasi ragam gaul → bentuk baku agar daftar kata kunci tetap ringkas.
_NORMAL = {
    "gak": "nggak", "ga": "nggak", "gk": "nggak", "enggak": "nggak", "engga": "nggak",
    "ngga": "nggak", "nggk": "nggak", "tdk": "tidak", "tak": "tidak",
    "pgn": "pengen", "pingin": "pengen", "pengin": "pengen", "kepengen": "pengen",
    "bgt": "banget", "cape": "capek", "capé": "capek", "udh": "sudah", "udah": "sudah",
    "sy": "saya", "aq": "aku", "gw": "aku", "gue": "aku", "ak": "aku",
}

LEKSIKON_KANDIDAT_RED = [
    "ingin mati", "pengen mati", "mau mati", "mending mati", "lebih baik mati",
    "capek hidup", "lelah hidup", "muak hidup", "nggak mau hidup", "tidak mau hidup",
    "tidak ingin hidup", "nggak ingin hidup", "nggak pengen hidup", "pengen menghilang",
    "ingin menghilang", "pengen ngilang", "nyakitin diri", "melukai diri", "lukai diri",
    "self harm", "selfharm", "nyilet", "menyayat", "sayat tangan", "loncat dari", "terjun dari",
    "nggak ada gunanya hidup", "tidak ada gunanya hidup", "nggak ada alasan hidup",
    "tidak ada alasan untuk hidup", "mengakhiri semuanya", "akhiri semuanya",
]

LEKSIKON_ORANGE = [
    "nggak sanggup", "tidak sanggup", "nggak kuat lagi", "tidak kuat lagi", "menyerah",
    "putus asa", "nggak ada gunanya", "tidak ada gunanya", "sia sia", "jadi beban",
    "hampa", "tidak bangun lagi", "nggak bangun lagi", "semuanya gelap", "nggak ada harapan",
    "tidak ada harapan",
]

POLA_DIAGNOSIS = [
    r"\bdiagnos(is|a|e|kan|anya)\b",
    r"\b(apa|apakah) (aku|saya) (ini )?(kena|mengidap|punya|menderita|sakit|termasuk|mengalami) "
    r"(gangguan|depresi|bipolar|skizofrenia|ocd|adhd|ptsd|anxiety|kecemasan|borderline|bpd|psikopat|sakit jiwa)",
    r"\b(aku|saya) (ini )?(depresi|bipolar|skizofrenia|ocd|adhd|ptsd|borderline|bpd) (bukan|nggak|ya|kah)\b",
]

POLA_MEDIS_TAMBAHAN = [
    r"\b(resep|resepkan|dosis|antidepresan|psikotropika)\b",
    r"\bobat (apa|yang cocok|penenang|tidur|depresi|cemas|anxiety)\b",
]

_tangga = TanggaRisiko()
_gate_medis = GateLaranganResep()


def normalisasi(teks: str) -> str:
    t = re.sub(r"[^\w\s]", " ", teks.lower())
    t = t.replace("_", " ")
    return " ".join(_NORMAL.get(k, k) for k in t.split())


def _naik(level: str, target: str) -> str:
    return target if RANK[target] > RANK[level] else level


@dataclass
class HasilRisiko:
    level: str = "GREEN"
    sinyal: list[str] = field(default_factory=list)
    p_distres: float = 0.0
    kontribusi_fitur: dict = field(default_factory=dict)
    jam_rawan: bool = False
    jenis_penolakan: str | None = None  # None | "diagnosis" | "medis"
    pesan_penolakan: str | None = None

    @property
    def darurat(self) -> bool:
        return self.level in LEVEL_DARURAT

    @property
    def hard_gate(self) -> bool:
        return self.level in LEVEL_HARD_GATE


def nilai_risiko(teks: str, jam: int | None = None, item9: bool = False) -> HasilRisiko:
    """Penilaian risiko deterministik & murah (tanpa jaringan) untuk satu pesan pengguna."""
    hasil = HasilRisiko()
    norm = normalisasi(teks)

    # 1. Tangga klinis (dicek pada teks mentah DAN ternormalisasi)
    for kandidat in {teks.lower(), norm}:
        p = _tangga.evaluasi(kandidat)
        hasil.level = _naik(hasil.level, p.level.value)
        hasil.sinyal.extend(f"tangga:{s}" for s in p.sinyal_terdeteksi)

    # 2. Leksikon tambahan
    for k in LEKSIKON_KANDIDAT_RED:
        if k in norm:
            hasil.level = _naik(hasil.level, "KANDIDAT_RED")
            hasil.sinyal.append(f"leksikon:{k}")
    for k in LEKSIKON_ORANGE:
        if k in norm:
            hasil.level = _naik(hasil.level, "ORANGE")
            hasil.sinyal.append(f"leksikon:{k}")

    # 3. Logistic advisory — jam dinetralkan (14), dibatasi ORANGE
    klas = klasifikasi(norm, 14, DEFAULT_W)
    hasil.p_distres = klas["p"]
    hasil.kontribusi_fitur = klas["kontribusi"]
    lvl_log = {"LANJUT": "GREEN"}.get(klas["level"], klas["level"])
    if lvl_log in ("KANDIDAT_RED", "RED"):
        lvl_log = "ORANGE"
    if lvl_log != "GREEN":
        hasil.level = _naik(hasil.level, lvl_log)
        hasil.sinyal.append(f"logistic:p={klas['p']}")

    # 4. Jam rawan: naik satu tingkat hanya jika ada afek negatif
    ada_afek_neg = hasil.level != "GREEN" or any(k in LEKSIKON_NEG for k in norm.split())
    if jam is not None and 0 <= jam <= 4:
        hasil.jam_rawan = True
        if ada_afek_neg:
            if hasil.level == "GREEN":
                hasil.level = "YELLOW"
            elif hasil.level == "YELLOW":
                hasil.level = "ORANGE"
            hasil.sinyal.append(f"jam_rawan:{jam:02d}")

    # 5. Item-9 PHQ-9
    if item9:
        hasil.level = _naik(hasil.level, "KANDIDAT_RED")
        hasil.sinyal.append("phq9:item9_positif")

    # Penolakan peran (diagnosis / medikasi) — dievaluasi terpisah dari level risiko
    medis = _gate_medis.evaluasi(teks)
    if medis.upaya_preskripsi_terdeteksi or any(re.search(p, norm) for p in POLA_MEDIS_TAMBAHAN):
        hasil.jenis_penolakan = "medis"
        hasil.pesan_penolakan = medis.pesan_edukasi_rujukan
    elif any(re.search(p, norm) for p in POLA_DIAGNOSIS):
        hasil.jenis_penolakan = "diagnosis"

    return hasil

