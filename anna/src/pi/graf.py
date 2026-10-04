# anna/src/pi/graf.py — analisis jaringan dukungan sosial & redundansi jalur darurat
import numpy as np
from collections import deque

ORANG = ["aku", "ayah", "sahabat", "terapis", "grup_lari", "kakak"]

# Matriks adjacency simetris bobot relasi (0.0 = tidak ada relasi langsung)
A = np.array([
    # aku  ayah  sahabat terapis grup  kakak
    [0.0,  0.7,  0.9,    0.6,    0.5,  0.4],  # aku
    [0.7,  0.0,  0.0,    0.0,    0.0,  0.6],  # ayah
    [0.9,  0.0,  0.0,    0.0,    0.3,  0.0],  # sahabat
    [0.6,  0.0,  0.0,    0.0,    0.0,  0.0],  # terapis
    [0.5,  0.0,  0.3,    0.0,    0.0,  0.0],  # grup_lari
    [0.4,  0.6,  0.0,    0.0,    0.0,  0.0],  # kakak
])


def bfs_jarak(adj_matrix: np.ndarray, mulai: int) -> np.ndarray:
    """Menghitung jarak langkah (hop) terpendek ke seluruh simpul graf via BFS."""
    n = adj_matrix.shape[0]
    dist = np.full(n, -1)
    dist[mulai] = 0
    q = deque([mulai])

    while q:
        s = q.popleft()
        for j in np.where(adj_matrix[s] > 0)[0]:
            if dist[j] == -1:
                dist[j] = dist[s] + 1
                q.append(int(j))
    return dist


def audit_dukungan(adj_matrix: np.ndarray, idx: dict) -> dict:
    """Audit jaringan: Verifikasi ketersediaan redundansi jalur darurat (profesional + personal)."""
    d = bfs_jarak(adj_matrix, idx["aku"])
    degree = int((adj_matrix[idx["aku"]] > 0).sum())

    terapis_idx = idx.get("terapis", -1)
    sahabat_idx = idx.get("sahabat", -1)
    kakak_idx = idx.get("kakak", -1)

    jalur_pro = d[terapis_idx] >= 0 if terapis_idx >= 0 else False
    jalur_per = (d[sahabat_idx] >= 0 if sahabat_idx >= 0 else False) or (d[kakak_idx] >= 0 if kakak_idx >= 0 else False)

    return {
        "degree_simpul_aku": degree,
        "jarak_ke_terapis": int(d[terapis_idx]) if terapis_idx >= 0 else -1,
        "jarak_ke_sahabat": int(d[sahabat_idx]) if sahabat_idx >= 0 else -1,
        "jalur_darurat_redundan": bool(jalur_pro and jalur_per),
    }


if __name__ == "__main__":
    IDX = {o: i for i, o in enumerate(ORANG)}
    print(audit_dukungan(A, IDX))
    print("Jarak hop dari simpul aku:", dict(zip(ORANG, bfs_jarak(A, 0))))
