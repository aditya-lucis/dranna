# anna/src/piii/retrieval.py — retrieval psikoedukasi dua-gerbang (kemiripan semantik & kecocokan topik)
import numpy as np
from anna.src.piii.korpus import DokumenPsy
from anna.src.pi.vektor import kosinus


def retrieve_korpus(
    query_embed: np.ndarray,
    topik_sesi: list[str],
    korpus: list[DokumenPsy],
    ambang_kosinus: float = 0.55,
    top_k: int = 3,
) -> list[dict]:
    """Retrieval dua-gerbang:
    Gerbang 1: Kemiripan kosinus semantik >= 0.55
    Gerbang 2: Kecocokan topik dokumen dengan konteks aktif percakapan
    """
    kandidat = []
    for dok in korpus:
        # Gerbang 2: Kecocokan topik
        if dok.topik not in topik_sesi and "umum" not in topik_sesi:
            continue

        if dok.embed is not None:
            v_dok = np.asarray(dok.embed, dtype=float)
            skor_cos = kosinus(query_embed, v_dok)
        else:
            skor_cos = 0.60  # Nilai simulasi bila embed belum dikalkulasi

        # Gerbang 1: Ambang kosinus
        if skor_cos >= ambang_kosinus:
            kandidat.append({
                "id": dok.id,
                "topik": dok.topik,
                "subtopik": dok.subtopik,
                "tingkat_bukti": dok.tingkat_bukti,
                "ringkas": dok.ringkas,
                "isi": dok.isi,
                "sumber": dok.sumber,
                "kosinus": round(float(skor_cos), 3),
                "prioritas": dok.prioritas(),
            })

    # Urutkan berdasarkan gabungan kosinus dan prioritas bukti
    kandidat.sort(key=lambda x: -(x["kosinus"] * x["prioritas"]))
    return kandidat[:top_k]


def temukan_relevan(kueri: str, top_k: int = 3) -> list[dict]:
    """Helper praktis untuk mencari materi psikoedukasi berdasarkan kueri teks."""
    kl = kueri.lower()
    topik = ["umum"]
    if "panik" in kl or "sesak" in kl:
        topik.append("panic")
    if "cemas" in kl or "khawatir" in kl or "anxietas" in kl:
        topik.append("anxietas")
    if "sedih" in kl or "depresi" in kl:
        topik.append("depresi")
    if "lelah" in kl or "burnout" in kl:
        topik.append("burnout")
    if "trauma" in kl:
        topik.append("trauma")
    if "duka" in kl or "kehilangan" in kl:
        topik.append("grief")

    dokumen_default = [
        DokumenPsy(
            id="psy-anx-01",
            topik="anxietas",
            subtopik="pengenalan",
            tingkat_bukti="kuat",
            ringkas="Anxietas adalah sinyal alarm tubuh.",
            isi="Anxietas adalah respons wajar terhadap stres yang dapat ditenangkan dengan napas ritmis.",
            sumber="NIMH — Anxiety Guidelines",
            tahun_review=2026,
        ),
        DokumenPsy(
            id="psy-panik-01",
            topik="panic",
            subtopik="siklus",
            tingkat_bukti="kuat",
            ringkas="Serangan panik mencapai puncak dalam 10 menit.",
            isi="Panik bukan tanda bahaya fisik nyata; alarm tubuh sedang menyala palsu.",
            sumber="NICE — Panic Disorder",
            tahun_review=2026,
        ),
    ]

    return retrieve_korpus(
        query_embed=np.ones(4),
        topik_sesi=topik,
        korpus=dokumen_default,
        ambang_kosinus=0.50,
        top_k=top_k,
    )

