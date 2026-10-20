# anna/src/piii/prompt_burnout.py — edukasi burnout di graph (pemilih topik)

def pilih_dokumen_burnout(konteks: dict) -> list[str]:
    """Memilih dokumen burnout sesuai nuansa keluhan pengguna."""
    dok = ["burn-apa-itu"]
    if konteks.get("sinis_terhadap_pekerjaan"):
        dok.append("burn-dimensi-cynicism")
    if konteks.get("meluas_ke_ranah_pribadi"):
        dok.append("burn-vs-depresi")  # + tawaran refleksi PHQ-9
    return dok
