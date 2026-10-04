# anna/tests/test_vektor.py — pengujian aljabar linear ruang vektor semantik
import numpy as np
from anna.src.pi.vektor import cari_terdekat, kosinus, normalisasi


def test_kosinus_identitas_dan_orthogonal():
    """Aljabar linear: Sudut kosinus vektor terhadap dirinya sendiri adalah 1, dan orthogonal adalah 0."""
    u = np.array([1.0, 0.0])
    assert abs(kosinus(u, u) - 1.0) < 1e-9
    assert abs(kosinus(u, np.array([0.0, 1.0]))) < 1e-9


def test_normalisasi_batas_nol():
    """Invarian: Baris non-nol memiliki norma L2 tepat 1.0, sedangkan vektor nol tetap dipertahankan nol."""
    V = np.array([[3.0, 4.0], [0.0, 0.0]])
    N = normalisasi(V)
    assert np.allclose(np.linalg.norm(N[0]), 1.0)
    assert np.allclose(N[1], 0.0)


def test_cari_terdekat_menemukan_sisi():
    """Retrieval: Pencarian dokumen paling serupa menemukan tetangga terdekat dengan tepat."""
    rng = np.random.default_rng(2)
    korpus = rng.normal(0, 1, (10, 4))
    q = korpus[7] + rng.normal(0, 0.1, 4)
    assert cari_terdekat(q, korpus, top=1)[0][0] == 7
