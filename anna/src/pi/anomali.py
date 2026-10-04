# anna/src/pi/anomali.py — deteksi hari tak-biasa via residu PCA dan ambang MAD
import numpy as np
from anna.src.pi.pca import residu_pca


def deteksi_hari_tak_biasa(X: np.ndarray, k: int = 2) -> list[int]:
    """Deteksi hari anomali via residu PCA dengan ambang batas Median Absolute Deviation (MAD).
    MAD digunakan (bukan std) agar hari ekstrem tidak menggeser ambang deteksinya sendiri.
    """
    res = residu_pca(X, k=k)
    med = float(np.median(res))
    mad = float(np.median(np.abs(res - med)))
    ambang = med + 3.0 * 1.4826 * mad
    return [i for i, r in enumerate(res) if r > ambang]
