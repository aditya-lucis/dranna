# anna/src/pi/fsm.py — Finite State Machine percakapan dengan matriks transisi & histeresis
import numpy as np

STATE = ["MENYAPA", "MENDENGARKAN", "SKRINING", "GROUNDING", "REFLEKSI", "SELESAI"]
IDX = {s: i for i, s in enumerate(STATE)}

# Matriks transisi legal boolean |S| x |S|
T = np.zeros((len(STATE), len(STATE)), dtype=bool)
TRANSISI = [
    ("MENYAPA", "MENDENGARKAN"),
    ("MENDENGARKAN", "MENDENGARKAN"),
    ("MENDENGARKAN", "SKRINING"),
    ("MENDENGARKAN", "REFLEKSI"),
    ("SKRINING", "GROUNDING"),
    ("SKRINING", "SELESAI"),
    ("GROUNDING", "SKRINING"),
    ("GROUNDING", "REFLEKSI"),
    ("REFLEKSI", "MENDENGARKAN"),
    ("REFLEKSI", "SELESAI"),
    ("SELESAI", "MENYAPA"),
]

for a, b in TRANSISI:
    T[IDX[a], IDX[b]] = True


def bfs_reachable(trans_matrix: np.ndarray, mulai: int) -> set[int]:
    """Pencarian keterjangkauan state via Breadth-First Search (BFS)."""
    dilihat, antrian = {mulai}, [mulai]
    while antrian:
        s = antrian.pop(0)
        for j in np.where(trans_matrix[s])[0]:
            if j not in dilihat:
                dilihat.add(int(j))
                antrian.append(int(j))
    return dilihat


def audit() -> dict:
    """Audit properti struktural FSM: reachability, ketiadaan state mati, dan invarian alur."""
    reachable = bfs_reachable(T, IDX["MENYAPA"])
    kolom_nol = [STATE[j] for j in np.where(~T.any(axis=0))[0]]
    # Invarian: Dari SKRINING dilarang langsung loncat ke REFLEKSI tanpa penyelesaian
    pelanggaran = T[IDX["SKRINING"], IDX["REFLEKSI"]]
    return {
        "semua_reachable": len(reachable) == len(STATE),
        "state_jalan_buntu": kolom_nol,
        "skrining_lompat_refleksi": bool(pelanggaran),
    }


def transisi(state: str, event: str) -> str:
    """Fungsi transisi delta: Transisi ilegal menolak bergerak (fail-safe)."""
    peta = {
        "sapaan": "MENYAPA",
        "cerita": "MENDENGARKAN",
        "sinyal_berat": "SKRINING",
        "setuju_grounding": "GROUNDING",
        "selesai_sesi": "SELESAI",
    }
    tujuan = peta.get(event)
    if tujuan is None or not T[IDX[state], IDX[tujuan]]:
        return state  # Fail-safe: tetap di state saat ini
    return tujuan


if __name__ == "__main__":
    print("Hasil audit FSM:", audit())
    print("Lompat ilegal MENYAPA -> GROUNDING:", transisi("MENYAPA", "setuju_grounding"))
