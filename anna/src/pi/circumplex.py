# anna/src/pi/circumplex.py — representasi emosi valence-arousal (Russell PAD)
import numpy as np

# Titik kalibrasi kata emosi umum (v, a) — heuristik desain kontinu [-1, 1]
KATA = {
    "senang": (0.8, 0.4),
    "tenang": (0.5, -0.5),
    "antusias": (0.7, 0.8),
    "sedih": (-0.6, -0.4),
    "mati_rasa": (-0.4, -0.8),
    "cemas": (-0.5, 0.6),
    "panik": (-0.8, 0.9),
    "marah": (-0.7, 0.7),
    "lelah": (-0.3, -0.6),
    "bangga": (0.6, 0.3),
}


def pad(kata: str) -> np.ndarray:
    """Mengembalikan koordinat (valence, arousal) untuk kata tertentu."""
    return np.array(KATA[kata], dtype=np.float64)


def jarak(k1: str, k2: str) -> float:
    """Jarak Euclidean antara dua titik emosi di ruang PAD."""
    return float(np.linalg.norm(pad(k1) - pad(k2)))


def kuadran(e: np.ndarray) -> str:
    """Partisi diskret ke 4 kuadran: energi (tinggi/rendah) - rasa (nyaman/tidak-nyaman)."""
    v, a = e[0], e[1]
    nyaman = "nyaman" if v >= 0 else "tidak-nyaman"
    energi = "tinggi" if a >= 0 else "rendah"
    return f"{energi}-{nyaman}"


def hitung_laju(trajektori: np.ndarray) -> np.ndarray:
    """Menghitung kecepatan pergeseran emosi antar hari."""
    return np.linalg.norm(np.diff(trajektori, axis=0), axis=1)


if __name__ == "__main__":
    trajektori = np.array([pad("sedih"), pad("mati_rasa"), pad("panik")])
    laju = hitung_laju(trajektori)
    print("jarak(sedih, marah) =", round(jarak("sedih", "marah"), 3))
    print("laju harinya        =", np.round(laju, 3))
    print("kuadran panik       =", kuadran(pad("panik")))
