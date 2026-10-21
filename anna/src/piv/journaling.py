# anna/src/piv/journaling.py — prompt journaling harian non-judgmental
import random
from langchain_core.tools import tool

PROMPT = [
    "Hari ini, apa yang terasa paling berat — tanpa harus dijelaskan?",
    "Satu hal kecil yang tidak kamu harapkan hari ini.",
    "Kalau perasaanmu hari ini punya warna, warna apa?",
    "Apa yang membuatmu bertahan hari ini — sekecil apa pun?",
    "Satu hal yang ingin kamu katakan ke dirimu sendiri besok pagi.",
]


def prompt_harian(seed=None) -> str:
    """Memilih prompt refleksi harian tanpa paksaan narasi atau optimisme beracun."""
    r = random.Random(seed)
    return r.choice(PROMPT) + " (boleh satu kata; boleh skip)"


@tool
def tawarkan_journaling() -> str:
    """Tawarkan prompt jurnal harian (opsional, tanpa vonis)."""
    return prompt_harian()
