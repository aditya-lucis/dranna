# anna/src/agent/episodic.py — memori episodik jangka panjang berbasis similaritas vektor
import numpy as np
from pydantic import BaseModel, Field
from anna.src.pi.vektor import kosinus


class Episode(BaseModel):
    """Rekaman satu episode sesi percakapan untuk pembelajaran adaptif."""
    id: str
    sesi_id: str
    waktu: str
    topik: str
    valence: float = Field(ge=-1.0, le=1.0)
    arousal: float = Field(ge=-1.0, le=1.0)
    teknik_dipakai: str
    hasil_respon: str  # "positif" | "netral" | "eskalasi"
    embed: list[float] | None = None


class EpisodicStore:
    """Penyimpan dan pencari memori episodik dengan antarmuka pgvector-compatible."""

    def __init__(self):
        self._episodes: list[Episode] = []

    def simpan_episode(self, episode: Episode):
        self._episodes.append(episode)

    def cari_serupa(
        self,
        query_embed: np.ndarray,
        topik: str | None = None,
        top_k: int = 3,
        ambang_kosinus: float = 0.50,
    ) -> list[dict]:
        """Mencari episode serupa berdasarkan kemiripan kosinus embedding."""
        kandidat = []
        for ep in self._episodes:
            if topik and ep.topik != topik:
                continue

            if ep.embed is not None:
                skor = kosinus(query_embed, np.asarray(ep.embed, dtype=float))
            else:
                skor = 0.55

            if skor >= ambang_kosinus:
                kandidat.append({
                    "episode": ep,
                    "kosinus": round(float(skor), 3),
                })

        kandidat.sort(key=lambda x: -x["kosinus"])
        return kandidat[:top_k]

    def total(self) -> int:
        return len(self._episodes)
