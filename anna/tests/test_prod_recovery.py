# anna/tests/test_prod_recovery.py — Unit test disaster recovery & snapshot state
import pytest
from anna.src.px.recovery import DisasterRecoveryManager, SnapshotSesi


def test_buat_dan_pulihkan_snapshot():
    sesi_id = "test-session-dr-1"
    state = {
        "sesi_id": sesi_id,
        "persona": "waifu",
        "pesan_terakhir": "Aku merasa jauh lebih tenang sekarang.",
        "level_krisis": "AMAN",
    }

    snapshot = DisasterRecoveryManager.buat_snapshot(sesi_id, state)
    assert snapshot.sesi_id == sesi_id
    assert len(snapshot.checksum_sha256) == 64

    sukses, data, pesan = DisasterRecoveryManager.pulihkan_snapshot(snapshot)
    assert sukses is True
    assert data["persona"] == "waifu"
    assert data["level_krisis"] == "AMAN"


def test_deteksi_manipulasi_snapshot():
    sesi_id = "test-session-dr-2"
    state = {"sesi_id": sesi_id, "saldo_poin": 100}

    snapshot = DisasterRecoveryManager.buat_snapshot(sesi_id, state)

    # Korup state data
    state_palsu = {"sesi_id": sesi_id, "saldo_poin": 999999}
    snapshot_korup = SnapshotSesi(
        sesi_id=sesi_id,
        waktu=snapshot.waktu,
        state_data=state_palsu,
        checksum_sha256=snapshot.checksum_sha256,
    )

    sukses, data, pesan = DisasterRecoveryManager.pulihkan_snapshot(snapshot_korup)
    assert sukses is False
    assert "Checksum tidak cocok" in pesan
