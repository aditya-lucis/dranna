# anna/src/pi/registry.py — registry cabang psikologi ke modul kode
REGISTRY = {
    "klinis": ["anna.src.klinik.phq9", "anna.src.krisis.tangga", "anna.src.pi.bayes"],
    "kognitif": ["anna.src.kognitif.anggaran", "anna.src.pi.attention"],
    "perkembangan": [],  # inspirasi panduan prompt saja
    "kepribadian": ["anna.src.pi.bigfive"],
    "sosial_positif": ["anna.src.terapi.perma", "anna.src.pi.graf"],
}


def jelaskan_sumber_perilaku(fitur: str) -> str:
    """Audit: fitur Anna menarik dari cabang psikologi mana."""
    sumber = {m: k for k, mods in REGISTRY.items() for m in mods}
    return sumber.get(fitur, "fitur tidak ditemukan / butuh registrasi")
