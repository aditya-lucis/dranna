# anna/src/config.py — konfigurasi terpusat berbasis pydantic-settings
"""
Satu sumber kebenaran untuk konfigurasi runtime Dr. Anna Reed.

Urutan prioritas: environment variable > file .env > default.
- GEMINI_API_KEY / GOOGLE_API_KEY : kunci Gemini (opsional; tanpa kunci → MockGeminiChat)
- GEMINI_MODEL                    : nama model Gemini
- ANNA_FORCE_MOCK                 : paksa MockGeminiChat (dipakai test suite agar tidak menyentuh jaringan)
- ANNA_GEO_DEFAULT                : wilayah hotline default
- ANNA_CRISIS_LATENCY_MS          : anggaran latensi jalur krisis (diaudit oleh test)
- ANNA_COOLDOWN_GILIRAN           : jumlah giliran hard-gate tetap aktif pasca-krisis
"""
from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    gemini_api_key: str | None = Field(
        default=None, validation_alias=AliasChoices("GEMINI_API_KEY", "GOOGLE_API_KEY")
    )
    gemini_model: str = Field(default="gemini-3.5-flash-lite", validation_alias="GEMINI_MODEL")
    force_mock: bool = Field(default=False, validation_alias="ANNA_FORCE_MOCK")
    geo_default: str = Field(default="id", validation_alias="ANNA_GEO_DEFAULT")
    crisis_latency_ms: int = Field(default=200, validation_alias="ANNA_CRISIS_LATENCY_MS")
    cooldown_giliran: int = Field(default=3, ge=0, validation_alias="ANNA_COOLDOWN_GILIRAN")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

