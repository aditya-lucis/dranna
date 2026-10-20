# tools/korpus_audit.py — audit konsistensi korpus psikoedukasi untuk CI


def audit_korpus(dokumen: list[dict], tahun_sekarang: int = 2026) -> dict:
    """Memvalidasi integritas korpus psikoedukasi:
    1. Sumber wajib hadir
    2. Reviewer medis wajib hadir
    3. Usia dokumen <= 2 tahun (24 bulan)
    4. Label tingkat bukti 'kuat' wajib memiliki rujukan otoritas kredibel (NIMH, NICE, WHO)
    """
    masalah = []
    for d in dokumen:
        doc_id = d.get("id", "tanpa-id")
        if not d.get("sumber"):
            masalah.append((doc_id, "tanpa sumber"))
        if not d.get("reviewer"):
            masalah.append((doc_id, "tanpa reviewer"))

        usia = tahun_sekarang - d.get("tahun_review", 0)
        if usia > 2:
            masalah.append((doc_id, f"usia {usia} tahun-review"))

        sumber = d.get("sumber", "")
        if d.get("tingkat_bukti") == "kuat" and not (
            "NIMH" in sumber or "NICE" in sumber or "WHO" in sumber
        ):
            masalah.append((doc_id, "label kuat tanpa sumber besar"))

    return {
        "jumlah": len(masalah),
        "masalah": masalah,
        "lolos": len(masalah) == 0,
    }


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    from anna.src.piii.anxietas import KORPUS_ANX
    from anna.src.piii.depresi import KORPUS_DEP
    from anna.src.piii.burnout import KORPUS_BURNOUT
    from anna.src.piii.stres import KORPUS_STRES
    from anna.src.piii.trauma import KORPUS_TRAUMA
    from anna.src.piii.panik import KORPUS_PANIK
    from anna.src.piii.grief import KORPUS_GRIEF
    from anna.src.piii.loneliness import KORPUS_LONELINESS
    from anna.src.piii.selfesteem import KORPUS_SELFESTEEM
    from anna.src.piii.tidur import KORPUS_TIDUR

    semua_dok = (
        KORPUS_ANX
        + KORPUS_DEP
        + KORPUS_BURNOUT
        + KORPUS_STRES
        + KORPUS_TRAUMA
        + KORPUS_PANIK
        + KORPUS_GRIEF
        + KORPUS_LONELINESS
        + KORPUS_SELFESTEEM
        + KORPUS_TIDUR
    )
    dicts = [d.model_dump() for d in semua_dok]
    hasil = audit_korpus(dicts)
    print("Hasil audit korpus aktif:", hasil)
    if not hasil["lolos"]:
        exit(1)
