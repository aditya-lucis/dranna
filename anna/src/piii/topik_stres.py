# anna/src/piii/topik_stres.py — pemilihan dokumen stres berbasis rule-out medis

def dokumen_stres(konteks: dict) -> list[str]:
    """Memilih topik stres dengan prioritas investigasi somatik medis."""
    dok = ["str-allostasis"]
    if konteks.get("somatik"):
        dok.append("str-somatik-rule-out")  # Medis dulu!
    if konteks.get("berbulan"):
        dok.append("str-kronik-rujuk")
    return dok
