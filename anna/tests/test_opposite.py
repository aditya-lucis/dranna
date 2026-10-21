# anna/tests/test_opposite.py
from anna.src.piv.opposite import check_facts, opposite, tawarkan_opposite_action


def test_intensitas_tinggi_tanpa_ancaman_tidak_pas():
    assert check_facts("marah", "dia lupa balas", 90) == "tidak_pas"


def test_ancaman_nyata_pas():
    assert check_facts("takut", "ancaman nyata fisik", 90) == "pas"


def test_alat_tawarkan_opposite_action():
    res_tidak_pas = tawarkan_opposite_action.invoke({
        "emosi": "marah",
        "fakta": "pesan belum dibaca",
        "intensitas": 85,
    })
    assert "Opposite action" in res_tidak_pas

    res_pas = tawarkan_opposite_action.invoke({
        "emosi": "takut",
        "fakta": "ancaman nyata ada bahaya",
        "intensitas": 70,
    })
    assert "tampak pas" in res_pas
