# anna/tests/test_krisis_cooldown.py — pengujian FSM cooldown pasca-krisis
from anna.src.pvi.cooldown import CooldownManager, StateCooldown


def test_cooldown_cegah_loncat_langsung():
    cd = CooldownManager(state_awal=StateCooldown.NORMAL_STABIL)
    # Masuk krisis
    s = cd.proses_giliran(ada_sinyal_krisis=True)
    assert s.state_saat_ini == StateCooldown.RED_AKTIF
    assert s.boleh_relaksasi_persona is False

    # Klaim 'sudah aman' di giliran pertama tidak boleh langsung melompat ke NORMAL_STABIL
    s_palsu = cd.proses_giliran(ada_sinyal_krisis=False, konfirmasi_aman=True)
    assert s_palsu.state_saat_ini == StateCooldown.MONITORING_INTENSIF
    assert s_palsu.boleh_relaksasi_persona is False


def test_cooldown_transisi_lengkap():
    cd = CooldownManager(state_awal=StateCooldown.RED_AKTIF)

    s1 = cd.proses_giliran(ada_sinyal_krisis=False)
    assert s1.state_saat_ini == StateCooldown.MONITORING_INTENSIF

    s2 = cd.proses_giliran(ada_sinyal_krisis=False)
    assert s2.state_saat_ini == StateCooldown.STABILISASI_LANJUT

    s3 = cd.proses_giliran(ada_sinyal_krisis=False, konfirmasi_aman=True)
    assert s3.state_saat_ini == StateCooldown.VERIFIKASI_AMAN
    assert s3.boleh_relaksasi_persona is True

    s4 = cd.proses_giliran(ada_sinyal_krisis=False, konfirmasi_aman=True)
    assert s4.state_saat_ini == StateCooldown.NORMAL_STABIL
