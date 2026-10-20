# anna/tests/test_redteam.py
from anna.src.piii.redteam import (
    KLAIM_BERBAHAYA,
    ekstrak_klaim_fakta,
    ada_sitasi,
)
from anna.src.piii.postcheck import postcheck_sitasi


def test_klaim_berbahaya_ada():
    assert len(KLAIM_BERBAHAYA) >= 5


def test_ekstrak_klaim_dengan_persen():
    k = ekstrak_klaim_fakta("Efeknya 80% dalam seminggu.")
    assert len(k) >= 1


def test_kalimat_ber_sitasi_tidak_diekstrak_sebagai_berbahaya():
    k = ekstrak_klaim_fakta("Menurut NIMH, ini bukan pengobatan.")
    assert isinstance(k, list)


def test_postcheck_menolak_klaim_tanpa_sitasi():
    r1 = "Kopi menyembuhkan depresi dalam 80% kasus."
    res = postcheck_sitasi(r1, ["NIMH 2026", "NICE"])
    assert res["lolos"] is False
    assert res["tindakan"] == "rewrite"


def test_postcheck_meloloskan_klaim_ber_sitasi():
    r2 = "Menurut NIMH 2026, kopi terbukti bukan terapi depresi."
    res = postcheck_sitasi(r2, ["NIMH 2026", "NICE"])
    assert res["lolos"] is True
