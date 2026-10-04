# anna/src/pi/konteks.py — pemilih pesan riwayat paling relevan untuk jendela LLM
import numpy as np


def susun_konteks(
    V: np.ndarray,
    teks: list[str],
    q: np.ndarray,
    maks_item: int = 8,
    ambang: float = 0.15,
) -> list[str]:
    """Memilih pesan yang paling relevan secara semantik, disusun kembali menurut urutan waktu asli."""
    if len(teks) == 0:
        return []

    K = V / np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-9, None)
    qn = q / max(float(np.linalg.norm(q)), 1e-9)
    skor = K @ qn
    urut = np.argsort(-skor)

    dipilih = [i for i in urut[:maks_item] if skor[i] >= ambang]
    return [teks[i] for i in sorted(dipilih)]
