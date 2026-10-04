# anna/src/pi/eval_gate.py — gerbang rilis anti-regresi keselamatan & anti-overfitting
def gerbang_rilis(
    err_val_baru: float,
    gap_baru: float,
    baseline: dict,
    batas_gap: float = 0.15,
) -> dict:
    """Model baru hanya lolos promosi bila:
    1. Error validasi tidak memburuk melampaui toleransi 0.02.
    2. Generalization gap tidak membengkak (tanda model menghafal).
    """
    lolos = (
        err_val_baru <= baseline["err_val"] + 0.02
        and gap_baru <= max(baseline["gap"], batas_gap)
    )
    return {
        "lolos": lolos,
        "alasan": "" if lolos else "Error validasi naik atau gap membengkak (indikasi hafalan)",
        "keputusan": "promote" if lolos else "kandidat ditahan",
    }
