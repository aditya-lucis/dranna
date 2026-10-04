# anna/src/pii/reflection.py — evaluasi kualitas refleksi (anti-parroting & anti-belok)
import numpy as np


def overlap_leksikal(a: str, b: str) -> float:
    """Menghitung Jaccard similarity kata unik antara dua teks."""
    sa = set(a.lower().split())
    sb = set(b.lower().split())
    if not (sa | sb):
        return 0.0
    return float(len(sa & sb) / max(len(sa | sb), 1))


def jenis_reflection(
    reflection: str,
    pesan: str,
    cos_semantik: float = 0.60,
) -> dict:
    """Mengklasifikasikan jenis refleksi:
    - PARROT: Overlap leksikal > 0.85 (hanya membeo kata pengguna)
    - BELOK: Kesamaan kosinus semantik < 0.25 (melenceng jauh dari maksud)
    - COMPLEX: Menambahkan satu dimensi makna tersirat (kosinus > 0.75)
    - SIMPLE: Memantulkan maksud pengguna secara netral (0.25 <= cos <= 0.75)
    """
    lap = overlap_leksikal(reflection, pesan)
    if lap > 0.85:
        return {"jenis": "PARROT", "masalah": "menyalin kata"}
    if cos_semantik < 0.25:
        return {"jenis": "BELOK", "masalah": "meninggalkan maksud"}
    if cos_semantik > 0.75:
        return {"jenis": "COMPLEX", "dimensi": "menambah makna"}
    return {"jenis": "SIMPLE", "dimensi": "netral-verifikasi"}


if __name__ == "__main__":
    pesan = "aku capek banget sama kerjaan, rasanya nggak pernah selesai"
    print("parrot :", jenis_reflection("aku capek banget sama kerjaan rasanya nggak pernah selesai", pesan, 0.90))
    print("belok  :", jenis_reflection("kamu marah ke atasanmu dan ingin resign", pesan, 0.18))
    print("sehat  :", jenis_reflection("kerjaanmu terasa tidak berkesudahan akhir-akhir ini", pesan, 0.68))
