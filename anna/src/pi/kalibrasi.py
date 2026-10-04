# anna/src/pi/kalibrasi.py — Expected Calibration Error (ECE) untuk keyakinan model
import numpy as np


def ece(yakin: np.ndarray, benar: np.ndarray, n_bin: int = 5) -> float:
    """Expected Calibration Error (ECE) dari keyakinan dan kebenaran.
    Jika ECE > 0.10, model overconfident dan dilarang memakai kata 'yakin'.
    """
    yakin = np.asarray(yakin, dtype=float)
    benar = np.asarray(benar, dtype=float)
    n = len(yakin)
    if n == 0:
        return 0.0

    bin_edge = np.linspace(0.0, 1.0, n_bin + 1)
    e = 0.0

    for b in range(n_bin):
        m = (yakin > bin_edge[b]) & (yakin <= bin_edge[b + 1])
        if m.sum() == 0:
            continue
        acc = float(benar[m].mean())
        conf = float(yakin[m].mean())
        e += (m.sum() / n) * abs(acc - conf)

    return round(float(e), 3)


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    yakin = rng.uniform(0.55, 0.95, 500)
    benar = rng.random(500) < (yakin * 0.65)  # Overconfident
    print("ECE (overconfident):", ece(yakin, benar))

    benar2 = rng.random(500) < yakin  # Terkalibrasi baik
    print("ECE (terkalibrasi) :", ece(yakin, benar2))
