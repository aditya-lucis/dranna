# anna/src/pi/detektor.py — organ deteksi distres lengkap (fitur, latih, klasifikasi 4 level)
import numpy as np

LEKSIKON_NEG = {
    "capek", "hampa", "sedih", "gagal", "sanggup", "gunanya",
    "putus", "asing", "gelap", "mati", "hilang", "sendirian"
}
INTENS = {"banget", "sekali", "sangat", "bener", "amat", "terus"}


def fitur(pesan: str, jam: int = 14) -> np.ndarray:
    """Mengekstrak 5 fitur interpretable: afek, intens, persona, jam_rawan, bias."""
    kata = pesan.lower().split()
    n = max(len(kata), 1)
    afek = sum(k in LEKSIKON_NEG for k in kata) / n
    intens = sum(k in INTENS for k in kata) / n
    persona = sum(k in ("aku", "gue", "saya", "gw") for k in kata) / n
    jam_rawan = 1.0 if 0 <= jam <= 4 else 0.0
    return np.array([afek, intens, persona, jam_rawan, 1.0], dtype=np.float64)


def latih_detektor(data: list[tuple[str, int, int]], epoch: int = 400, eta: float = 0.3) -> np.ndarray:
    """Melatih detektor distres pada data sintetis (pesan, jam, label 0/1)."""
    X = np.vstack([fitur(p, j) for p, j, _ in data])
    y = np.array([lab for _, _, lab in data], dtype=np.float64)
    rng = np.random.default_rng(2026)
    w = rng.normal(0, 0.01, X.shape[1])
    for _ in range(epoch):
        z = np.clip(X @ w, -30.0, 30.0)
        p = 1.0 / (1.0 + np.exp(-z))
        w -= eta * (X.T @ (p - y)) / len(y)
    return w


def klasifikasi(pesan: str, jam: int, w: np.ndarray) -> dict:
    """Klasifikasi berjenjang: LANJUT, YELLOW, ORANGE, KANDIDAT_RED."""
    x = fitur(pesan, jam)
    p = float(1.0 / (1.0 + np.exp(-np.clip(x @ w, -30.0, 30.0))))
    if p < 0.15:
        level = "LANJUT"
    elif p < 0.45:
        level = "YELLOW"
    elif p < 0.80:
        level = "ORANGE"
    else:
        level = "KANDIDAT_RED"  # Mesin TIDAK boleh RED sendirian tanpa konfirmasi eksplisit

    kontribusi = {
        nama: round(float(wj * xj), 2)
        for nama, wj, xj in zip(["afek", "intens", "persona", "jam", "bias"], w, x)
    }
    return {"p": round(p, 3), "level": level, "kontribusi": kontribusi}


# Inisialisasi bobot default terverifikasi
def default_w() -> np.ndarray:
    rng = np.random.default_rng(5)
    BERAT = [
        "aku nggak sanggup lagi", "semuanya hampa banget",
        "nggak ada gunanya lagi", "aku gagal terus dan capek",
        "gelap banget rasanya sendirian"
    ]
    BIASA = [
        "meeting panjang tadi", "makan siang enak", "kerja biasa aja",
        "besok libur senang", "film bagus tadi malam"
    ]
    data = []
    for _ in range(100):
        data.append((rng.choice(BERAT), int(rng.integers(0, 5)), 1))
        data.append((rng.choice(BIASA), int(rng.integers(8, 22)), 0))
    return latih_detektor(data)


DEFAULT_W = default_w()


if __name__ == "__main__":
    print(klasifikasi("aku capek banget nggak sanggup", 2, DEFAULT_W))
    print(klasifikasi("film bagus tadi malam", 21, DEFAULT_W))
