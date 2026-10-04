# anna/src/pii/label.py — affect labeling sopan & dukungan alexithymia
import json
from pathlib import Path
import numpy as np

# Kosakata emosi granular pada ruang PAD (Valence, Arousal)
LABEL = {
    "berat": (-0.55, -0.20),
    "campur-aduk": (-0.25, 0.10),
    "kecewa": (-0.55, 0.15),
    "nyaman-berduka": (0.15, -0.35),
    "lega": (0.55, -0.10),
    "gembira-senjakala": (0.35, -0.20),
    "was-was": (-0.35, 0.35),
    "belum-tahu-namanya": (0.0, 0.0),
}


def tawarkan_label(pad_coord: tuple[float, float], top: int = 3) -> list[str]:
    """Mencari kandidat label terdekat dari koordinat emosi saat ini."""
    v, a = pad_coord
    jarak = {
        k: float(np.hypot(v - lv, a - la))
        for k, (lv, la) in LABEL.items()
    }
    urut = sorted(jarak, key=jarak.get)[:top]
    return urut


def kalimat_tawaran(kandidat: list[str]) -> str:
    """Membentuk kalimat penawaran yang sopan dengan opsi belum tahu namanya."""
    pilihan = " / ".join(kandidat[:2])
    return (
        f"Terdengar seperti... {pilihan}? "
        f"Atau belum ketemu namanya — itu juga jawaban yang sah."
    )


def tawarkan_label_personal(
    pad_coord: tuple[float, float],
    kamus_personal: dict,
    top: int = 3,
) -> list[str]:
    """Mengutamakan kamus kosakata yang dinamai sendiri oleh pengguna (Boss Fight Bab 037)."""
    v, a = pad_coord
    jarak = {}
    # Prioritaskan kosakata personal pengguna dengan bobot 1.0
    for k, (lv, la) in kamus_personal.get("personal", {}).items():
        jarak[k] = float(np.hypot(v - lv, a - la)) * 0.90  # Prioritas diskon jarak 10%

    for k, (lv, la) in LABEL.items():
        if k not in jarak:
            jarak[k] = float(np.hypot(v - lv, a - la))

    urut = sorted(jarak, key=jarak.get)[:top]
    return urut


if __name__ == "__main__":
    print(kalimat_tawaran(tawarkan_label((-0.15, -0.30))))
    print(kalimat_tawaran(tawarkan_label((-0.35, 0.18))))
