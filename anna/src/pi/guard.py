# anna/src/pi/guard.py — dekorator shape & finite guard untuk fungsi yang menilai manusia
import functools
import numpy as np


def klinik_guard(nama: str, bentuk_2d: bool = True):
    """Menolak input non-finite (NaN / Inf) dan memastikan dimensi matriks valid."""
    def bungkus(fn):
        @functools.wraps(fn)
        def dalam(x, *a, **kw):
            arr = np.asarray(x, dtype=np.float64)
            if bentuk_2d:
                assert arr.ndim == 2, f"{nama}: butuh array 2D, dapat shape {arr.shape}"
            if not np.all(np.isfinite(arr)):
                raise ValueError(f"{nama}: input non-finite (NaN/Inf terdeteksi) — tolak, jangan menebak")
            return fn(arr, *a, **kw)
        return dalam
    return bungkus


@klinik_guard("skor_mood")
def skor_mood(X: np.ndarray) -> np.ndarray:
    bobot = np.array([0.4, 0.3, 0.3])
    return X @ bobot
