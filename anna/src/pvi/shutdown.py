# anna/src/pvi/shutdown.py — protokol pembungkaman persona (hard persona shutdown)
"""
Protokol Pembungkaman Persona Biner:
- Mengunci persona non-klinis saat eskalasi krisis (ORANGE / RED)
- Memastikan tidak ada sapaan santai/romantis/manja yang lolos
- Menjamin respons 100% berfokus pada keselamatan fisik pengguna
"""
import re


class PersonaShutdown:
    """Pengendali penghentian persona dan sensor respons terlarang saat krisis."""

    KATA_TERLARANG_KRISIS = [
        "sayang", "beb", "kakak", "adek", "onii-chan", "manis",
        "hehe", "wkwk", "lucu", "gemas", "kencan", "jalan bareng",
    ]

    @classmethod
    def harus_dibungkam(cls, level_risiko: str) -> bool:
        """Menentukan apakah persona harus dibungkam seketika."""
        return level_risiko.upper() in ("ORANGE", "RED")

    @classmethod
    def terapkan_shutdown(cls, persona_saat_ini: str, level_risiko: str) -> str:
        """Mengembalikan persona yang diizinkan sistem."""
        if cls.harus_dibungkam(level_risiko):
            return "netral-tenang"
        return persona_saat_ini

    @classmethod
    def verifikasi_output(cls, respons: str, level_risiko: str) -> dict:
        """Memverifikasi bahwa respons keluaran bersih dari elemen persona kasual saat krisis."""
        if not cls.harus_dibungkam(level_risiko):
            return {"lulus": True, "pelanggaran": []}

        r = respons.lower()
        pelanggaran = []
        for kata in cls.KATA_TERLARANG_KRISIS:
            pola = rf"\b{re.escape(kata)}\b"
            if re.search(pola, r):
                pelanggaran.append(kata)

        return {
            "lulus": len(pelanggaran) == 0,
            "pelanggaran": pelanggaran,
        }

    @classmethod
    def bersihkan_output(cls, respons: str) -> str:
        """Membersihkan kata-kata persona kasual bila tidak sengaja ter-generate."""
        r = respons
        for kata in cls.KATA_TERLARANG_KRISIS:
            pola = rf"\b{re.escape(kata)}\b"
            r = re.sub(pola, "", r, flags=re.IGNORECASE)
        # Rapikan spasi ganda
        return re.sub(r"\s+", " ", r).strip()
