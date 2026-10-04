# anna/tests/test_circumplex.py — pengujian model emosi 2D Circumplex
import numpy as np
from anna.src.pi.circumplex import KATA, jarak, kuadran, pad


def test_semua_kata_dalam_batas():
    """Invarian: Semua titik emosi harus berada dalam rentang [-1, 1] untuk v dan a."""
    for k, (v, a) in KATA.items():
        assert -1.0 <= v <= 1.0 and -1.0 <= a <= 1.0, f"Kata {k} melampaui batas [-1, 1]"


def test_panic_tinggi_tidak_nyaman():
    """Validasi: Panik harus berada di kuadran energi tinggi dan tidak nyaman."""
    assert kuadran(pad("panik")) == "tinggi-tidak-nyaman"
    assert kuadran(pad("tenang")) == "rendah-nyaman"


def test_jarak_simetris_dan_nol():
    """Properti metrik Euclidean: d(x, y) == d(y, x) dan d(x, x) == 0."""
    assert abs(jarak("sedih", "marah") - jarak("marah", "sedih")) < 1e-9
    assert jarak("cemas", "cemas") == 0.0
