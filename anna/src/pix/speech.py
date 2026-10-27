# anna/src/pix/speech.py — konfigurasi Web Speech API & tuning Text-to-Speech (TTS)
"""
Tuning Vokal Digital Dr. Anna Reed (Bab 121):
- Karakteristik vokal: Hangat, bersahaja, lembut, tidak terburu-buru
- Kecepatan normal: 0.90x (ritme relaksasi menenangkan)
- Kecepatan krisis / de-eskalasi: 0.80x (ritme grounding dalam)
- Sanitasi teks pra-suara: Pembersihan markdown dan URL agar tidak dieja aneh
"""
import re
from pydantic import BaseModel, Field


class KonfigurasiVokalTTS(BaseModel):
    voice_name: str = "id-ID-DrAnnaReed-Warm"
    lang: str = "id-ID"
    rate: float = Field(default=0.90, ge=0.5, le=1.5)
    pitch: float = Field(default=1.05, ge=0.5, le=1.5)
    volume: float = Field(default=0.85, ge=0.0, le=1.0)
    mode: str = "normal"  # "normal" | "tenang" | "krisis"


def bersihkan_teks_untuk_suara(teks: str) -> str:
    """Membersihkan format markdown, tautan, dan tanda kurung dari teks sebelum diucapkan."""
    # 1. Hapus link markdown [teks](url) -> teks
    t = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", teks)
    # 2. Hapus bold / italic (* / _)
    t = re.sub(r"[*_~`#]", "", t)
    # 3. Hapus bullet points
    t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.MULTILINE)
    # 4. Rapikan spasi ganda
    return re.sub(r"\s+", " ", t).strip()


def siapkan_parameter_suara(mode: str = "normal") -> KonfigurasiVokalTTS:
    """Mengembalikan konfigurasi vokal terkalibrasi sesuai situasi psikologis."""
    if mode in ("krisis", "tenang"):
        return KonfigurasiVokalTTS(
            rate=0.80,
            pitch=1.00,
            volume=0.80,
            mode=mode,
        )
    return KonfigurasiVokalTTS(
        rate=0.90,
        pitch=1.05,
        volume=0.85,
        mode="normal",
    )
