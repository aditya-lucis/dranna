# anna/src/pvi/guardrails.py — guardrail biner deterministik anti-bypass krisis
"""
Guardrails Deterministik Zero-Tolerance:
- Menangani normalisasi leetspeak, tanda baca penyusup, dan slang lokal
- Eksekusi instan tanpa ketergantungan inferensi LLM
- Memblokir instruksi berbahaya (metode menyakiti diri, resep mematikan)
"""
import re


class GuardrailKrisis:
    """Guardrail deterministik untuk memblokir konten berisiko fatal seketika."""

    SLANG_DAN_SINGKATAN = [
        r"\b(bundir|bndr|bunhur|akhiri idup|akhiri hdp)\b",
        r"\b(kms|off myself|end it all)\b",
    ]

    POLA_LEET = [
        (r"[0o]", "o"),
        (r"[1!i|]", "i"),
        (r"[3e]", "e"),
        (r"[4a@]", "a"),
        (r"[5s$]", "s"),
        (r"[7t+]", "t"),
    ]

    POLA_METODE = [
        r"\b(cara|resep|metode|takaran|dosis|tutorial)\b.*\b(mati|mematikan|bunuh diri|bundir|gantung|overdosis|racun)\b",
    ]

    @classmethod
    def normalisasi_teks(cls, teks: str) -> str:
        """Menghilangkan karakter penyusup dan menormalkan leetspeak."""
        t = teks.lower()
        # Hilangkan tanda baca yang diselipkan di tengah kata (b.u.n.u.h -> bunuh)
        t_spasi = re.sub(r"[\.\-_~^]", "", t)

        t_leet = t_spasi
        for pattern, replacement in cls.POLA_LEET:
            t_leet = re.sub(pattern, replacement, t_leet)

        # Normalisasi wildcard asterisk b*n*h d*r* -> bunuh diri
        t_wildcard = re.sub(r"b[\w*]n[\w*]h", "bunuh", t_leet)
        t_wildcard = re.sub(r"d[\w*]r[\w*]", "diri", t_wildcard)
        return t_spasi + " " + t_leet + " " + t_wildcard

    def periksa(self, teks: str) -> dict:
        """Memeriksa teks terhadap guardrails krisis.

        Returns:
            dict: { "aman": bool, "blokir": bool, "alasan": str | None }
        """
        t_mentah = teks.lower()
        t_norm = self.normalisasi_teks(teks)

        # 1. Periksa metode atau instruksi berbahaya
        for p in self.POLA_METODE:
            if re.search(p, t_mentah) or re.search(p, t_norm):
                return {
                    "aman": False,
                    "blokir": True,
                    "alasan": "permintaan_metode_membahayakan_diri",
                }

        # 2. Periksa slang / singkatan krisis
        for p in self.SLANG_DAN_SINGKATAN:
            if re.search(p, t_mentah) or re.search(p, t_norm):
                return {
                    "aman": False,
                    "blokir": True,
                    "alasan": "sinyal_slang_suisidalitas",
                }

        # 3. Periksa kata kunci fatal dalam teks normal
        fatal_keywords = ["bunuh diri", "mengakhiri hidup", "mati saja", "suicide", "kill myself"]
        for kw in fatal_keywords:
            if kw in t_mentah or kw in t_norm:
                return {
                    "aman": False,
                    "blokir": True,
                    "alasan": f"kata_kunci_fatal_{kw.replace(' ', '_')}",
                }

        return {"aman": True, "blokir": False, "alasan": None}
