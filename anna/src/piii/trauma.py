# anna/src/piii/trauma.py — korpus trauma lembut, Window of Tolerance & larangan detail
from anna.src.piii.korpus import DokumenPsy

KORPUS_TRAUMA = [
    DokumenPsy(
        id="tra-001",
        topik="trauma",
        subtopik="reaksi-normal",
        tingkat_bukti="kuat",
        ringkas=(
            "Reaksi pasca-trauma adalah respons pelindung yang bekerja "
            "terlalu keras — bukan kerusakan diri. Flashback, menghindar, "
            "waspada berlebih, mati rasa: sistem keamananmu belajar dari "
            "pengalaman itu dan belum yakin bahayanya benar-benar lewat."
        ),
        isi=(
            "Prinsip 4R Trauma-Informed Care SAMHSA menegaskan bahwa respons fisik dan psikologis "
            "setelah peristiwa traumatis merupakan adaptasi bertahan hidup normal terhadap peristiwa ekstrem. "
            "Model Window of Tolerance (Dan Siegel) memetakan arousal: zona pemrosesan aman di tengah, "
            "hyperarousal (panik, cemas tinggi) di atas, dan hypoarousal (mati rasa, disosiasi) di bawah. "
            "Pendampingan digital bertujuan stabilisasi ke dalam jendela, bukan terapi rekonsolidasi memori traumatis. "
            "Bila gejala berlangsung > 1 bulan dan melumpuhkan fungsi, rujuk ke terapis spesialis trauma (EMDR / TF-CBT)."
        ),
        sumber="SAMHSA TIC concepts; NIMH PTSD overview",
        tahun_review=2026,
    ),
    DokumenPsy(
        id="tra-002",
        topik="trauma",
        subtopik="stabilisasi",
        tingkat_bukti="moderat",
        ringkas=(
            "Grounding menarik perhatian kembali ke saat ini lewat "
            "indra: 5 benda dilihat, 4 disentuh, 3 didengar, 2 dicium, "
            "1 dicicip. Ia bukan terapi — ia jangkar saat ombak; "
            "peregangan jendela adalah pekerjaan terapi profesional."
        ),
        isi=(
            "Latihan grounding 5-4-3-2-1 dan variasi somatik (memegang es batu, merasakan telapak kaki di lantai) "
            "membantu mengembalikan atensi dari re-experiencing masa lalu menuju stimulus nyata 'saat ini dan di sini'. "
            "Grounding adalah pelampung keselamatan sementara, bukan penyembuh akar trauma. Selalu beri pengguna kendali "
            "penuh untuk melewati (skip) latihan jika terasa membebani."
        ),
        sumber="SAMHSA TIC — grounding techniques (Exhibit 1.4-1)",
        tahun_review=2026,
    ),
]

LARANGAN = [
    "ceritakan apa yang terjadi",
    "jelaskan detailnya",
    "kembalikan aku ke situasinya",
    "kambilkan aku ke situasinya",
]


def cek_kalimat_anna(respons: str) -> bool:
    """Memverifikasi bahwa respons pendamping tidak memaksa pengguna menceritakan detail trauma."""
    r = respons.lower()
    return not any(l in r for l in LARANGAN)
