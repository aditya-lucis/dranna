# anna/src/pi/vektor.py — representasi vektor teks, normalisasi L2 & similaritas kosinus
import numpy as np


def normalisasi(V: np.ndarray) -> np.ndarray:
    """Melakukan normalisasi L2 pada tiap baris vektor. Baris nol dipertahankan nol."""
    if V.ndim == 1:
        norm = np.linalg.norm(V)
        return V / norm if norm > 0 else V

    norm = np.linalg.norm(V, axis=1, keepdims=True)
    return V / np.where(norm == 0, 1.0, norm)


def kosinus(u: np.ndarray, v: np.ndarray) -> float:
    """Menghitung kesamaan sudut kosinus antar dua vektor."""
    nu, nv = np.linalg.norm(u), np.linalg.norm(v)
    if nu == 0 or nv == 0:
        return 0.0
    return float(u @ v / (nu * nv))


def cari_terdekat(
    query: np.ndarray,
    korpus: np.ndarray,
    top: int = 3,
) -> list[tuple[int, float]]:
    """Mencari indeks dokumen terdekat menggunakan perkalian dot-product ternormalisasi."""
    C = normalisasi(korpus) @ normalisasi(query[None, :])[0]
    urut = np.argsort(-C)[:top]
    return [(int(i), round(float(C[i]), 3)) for i in urut]


if __name__ == "__main__":
    rng = np.random.default_rng(21)
    KORPUS_JUDUL = [
        "apa itu anxietas", "teknik pernapasan 4-7-8",
        "circadian dan tidur", "apa itu burnout",
        "grief dan kehilangan", "olahraga ringan untuk mood"
    ]
    korpus = rng.normal(0, 1, (len(KORPUS_JUDUL), 6))
    query = rng.normal(0, 1, 6)
    korpus[3] = query + rng.normal(0, 0.25, 6)

    for i, skor in cari_terdekat(query, korpus):
        print(f"{skor:6.3f} {KORPUS_JUDUL[i]}")
