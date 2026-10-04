# anna/src/pi/embed.py — integrasi embedding Google Generative AI (text-embedding-004)
import numpy as np
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from anna.src.pi.vektor import normalisasi


def buat_embedder(model: str = "text-embedding-004") -> GoogleGenerativeAIEmbeddings:
    """Factory pembuat instans Google embedding 768 dimensi."""
    return GoogleGenerativeAIEmbeddings(model=model)


async def embed_teks(teks_list: list[str]) -> np.ndarray:
    """Mengubah daftar string menjadi matriks representasi vektor ternormalisasi L2."""
    embedder = buat_embedder()
    v = await embedder.aembed_documents(teks_list)
    return normalisasi(np.asarray(v, dtype=np.float32))
