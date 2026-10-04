# anna/src/pi/bigfive.py — vektor Big Five (OCEAN) & penyesuaian gaya
import numpy as np

SUMBU = ["O", "C", "E", "A", "N"]

# Profil default: netral — Anna TIDAK menebak sebelum ada data
PROFIL_DEFAULT = np.zeros(5)

GAYA = {
    "pendengar_tenang": np.array([0.0, 0.2, -0.6, 0.5, 0.3]),
    "ringan_playful": np.array([0.5, -0.2, 0.6, 0.2, -0.3]),
    "terstruktur_fokus": np.array([0.2, 0.8, 0.0, 0.0, -0.2]),
    "validasi_dahulu": np.array([0.1, 0.1, -0.2, 0.6, 0.6]),
}


def rekomendasi_gaya(p: np.ndarray, top: int = 2) -> list[tuple[str, float]]:
    """Kecocokan gaya bicara dihitung dari kesamaan kosinus profil vs vektor gaya."""
    norm_p = np.linalg.norm(p)
    if norm_p == 0:
        return [(k, 0.0) for k in list(GAYA.keys())[:top]]

    skor = {
        g: float(v @ p / (np.linalg.norm(v) * norm_p + 1e-9))
        for g, v in GAYA.items()
    }
    urut = sorted(skor.items(), key=lambda kv: -kv[1])
    return urut[:top]


def estimasi_bigfive(diari_percakapan: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """Estimator kepribadian yang tahu dirinya (Boss Fight Bab 015).
    Menghitung vektor p dan keyakinan per-sumbu.
    Sumbu dengan keyakinan di bawah 0.6 HARUS dikembalikan 0.0 (netral).
    """
    n_pesan = len(diari_percakapan)
    p = np.zeros(5, dtype=np.float64)
    keyakinan = np.zeros(5, dtype=np.float64)

    if n_pesan == 0:
        return p, keyakinan

    # Fitur sederhana
    total_kata = sum(len(m.split()) for m in diari_percakapan)
    avg_len = total_kata / n_pesan
    tanya_count = sum(m.count("?") for m in diari_percakapan)
    kata_pertama_persona = sum(
        m.lower().split()[0] in ("aku", "gue", "saya")
        for m in diari_percakapan if m.split()
    )

    # Keyakinan per-sumbu berdasar kecukupan data
    keyakinan[0] = min(n_pesan / 20.0, 1.0)  # Openness
    keyakinan[1] = min(n_pesan / 25.0, 1.0)  # Conscientiousness
    keyakinan[2] = min(n_pesan / 15.0, 1.0)  # Extraversion
    keyakinan[3] = min(n_pesan / 20.0, 1.0)  # Agreeableness
    keyakinan[4] = min(n_pesan / 15.0, 1.0)  # Neuroticism

    # Estimasi kasar bila keyakinan >= 0.6
    if keyakinan[2] >= 0.6:
        # Extraversion dari panjang pesan & interaksi
        p[2] = np.clip((avg_len - 15) / 10.0, -1.0, 1.0)
    if keyakinan[4] >= 0.6:
        # Neuroticism dari kepadatan pertanyaan dan persona
        p[4] = np.clip((tanya_count + kata_pertama_persona) / (n_pesan * 1.5), -1.0, 1.0)

    # Nol-kan yang keyakinannya kurang dari 0.6
    p = np.where(keyakinan >= 0.6, p, 0.0)
    return p, keyakinan


if __name__ == "__main__":
    preferensi_eksplisit = "pendengar_tenang"
    p_estimasi = np.array([0.2, 0.1, -0.5, 0.4, 0.7])
    print("estimasi saja :", rekomendasi_gaya(p_estimasi))
    print("yang dipakai  :", preferensi_eksplisit, "(eksplisit menang penuh)")
