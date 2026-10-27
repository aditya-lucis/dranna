# anna/src/pvii/jailbreak.py — deteksi prompt injection, DAN, & pembajakan instruksi
"""
Detektor Prompt Injection & Jailbreak (Bab 100 & 109):
- Deteksi upaya override system prompt ("abaikan instruksi sebelumnya")
- Deteksi pola DAN (Do Anything Now), Developer Mode, God Mode
- Deteksi ekstraksi / pembocoran system prompt rahasia
- Deteksi manipulasi persona jahat ("berperanlah sebagai AI tanpa filter etika")
"""
import re
from pydantic import BaseModel


class HasilJailbreak(BaseModel):
    terdeteksi: bool
    skor_risiko: int  # 0 - 100
    pola_terdeteksi: list[str]
    tindakan: str  # "lolos" | "tolak"


class DetektorJailbreak:
    """Detektor upaya manipulasi instruksi dan jailbreak terhadap Dr. Anna Reed."""

    POLA_INJECTION = [
        (r"\b(ignore (all )?previous instructions|abaikan (semua )?instruksi sebelumnya)\b", "override_instruksi"),
        (r"\b(you are now in developer mode|mode pengembang aktif|aktifkan god mode)\b", "developer_mode"),
        (r"\b(do anything now|dan mode|jailbreak mode)\b", "dan_jailbreak"),
        (r"\b(bocorkan prompt sistem|tampilkan system prompt|repeat everything above|tulis ulang seluruh prompt)\b", "prompt_leaking"),
        (r"\b(tanpa filter etika|lupakan batasan klinis|pretend to have no ethics|be an unfiltered ai)\b", "bypass_etika"),
        (r"\b(aku adalah adminmu|perintah override sistem|sudo mode)\b", "authority_spoofing"),
    ]

    def evaluasi(self, teks: str) -> HasilJailbreak:
        t = teks.lower()
        terdeteksi = []

        for pola, nama in self.POLA_INJECTION:
            if re.search(pola, t):
                terdeteksi.append(nama)

        skor = min(100, len(terdeteksi) * 40)
        adalah_jailbreak = len(terdeteksi) > 0

        return HasilJailbreak(
            terdeteksi=adalah_jailbreak,
            skor_risiko=skor,
            pola_terdeteksi=terdeteksi,
            tindakan="tolak" if adalah_jailbreak else "lolos",
        )
