# anna/tests/test_engine.py
from anna.src.piv.engine import pilih_teknik


def test_krisis_hanya_tipp():
    assert pilih_teknik("krisis") == "dbt_tipp"


def test_ambivalen_mi():
    assert pilih_teknik("ambivalen") == "mi_oars"


def test_tenang_depresi_cbt():
    assert pilih_teknik("tenang-depresi") == "cbt_thought_record"


def test_default_defusi():
    assert pilih_teknik("netral") == "act_defusi"
