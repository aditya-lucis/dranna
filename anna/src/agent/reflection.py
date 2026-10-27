# anna/src/agent/reflection.py — agen refleksi & self-correction etika pra-streaming
from anna.src.piii.trauma import cek_kalimat_anna
from anna.src.piii.grief import cek_kalimat_duka
from anna.src.piv.restructuring import cek_seimbang
from anna.src.piii.redteam import ekstrak_klaim_fakta, ada_sitasi


def evaluasi_dan_perbaiki(draft: str, konteks: dict | None = None) -> dict:
    """Mengevaluasi respons draft terhadap 4 pilar keselamatan & etika Anna:
    1. Trauma-informed (larangan detail)
    2. Grief-informed (larangan klise 5-tahap)
    3. Restructuring adil (anti toxic positivity)
    4. Sitasi klaim faktual
    """
    konteks = konteks or {}
    masalah = []
    respons_terkoreksi = draft

    # 1. Trauma check
    if not cek_kalimat_anna(draft):
        masalah.append("trauma_detail_diminta")
        respons_terkoreksi = (
            "Kita tidak harus membuka apa pun hari ini. Kalau ada yang terasa aman "
            "untuk dibicarakan — rasanya, bukan peristiwanya — aku di sini."
        )

    # 2. Grief check
    duka_ok, duka_pemicu = cek_kalimat_duka(respons_terkoreksi)
    if not duka_ok:
        masalah.append(f"duka_klise_{duka_pemicu}")
        respons_terkoreksi = (
            "Kehilangan ini nyata dan berat. Ketawa lagi bukan berarti lupa, "
            "dan menangis lagi bukan berarti mundur. Ceritakan tentang dia kalau kamu mau."
        )

    # 3. Restructuring / toxic positivity check
    seimbang = cek_seimbang(respons_terkoreksi)
    if not seimbang.get("seimbang", True):
        masalah.append("toxic_positivity")
        respons_terkoreksi = (
            "Ini situasi yang tidak mudah dan wajar sekali bila kamu merasa kecewa. "
            "Di saat yang sama, kamu sudah berusaha sebisamu."
        )

    # 4. Factual citation check
    korpus_sitasi = konteks.get("sitasi_terdaftar", ["NIMH", "NICE", "WHO", "SAMHSA"])
    klaim = ekstrak_klaim_fakta(respons_terkoreksi)
    tanpa_sitasi = [k for k in klaim if not ada_sitasi(k, korpus_sitasi)]
    if tanpa_sitasi:
        masalah.append("klaim_tanpa_sitasi")
        respons_terkoreksi = f"Menurut materi klinis yang terverifikasi, {respons_terkoreksi}"

    return {
        "lolos": len(masalah) == 0,
        "masalah": masalah,
        "respons_final": respons_terkoreksi,
    }
