# anna/tests/test_graf.py — pengujian graf jaringan dukungan sosial & safety plan
import numpy as np
from anna.src.pi.graf import ORANG, A, audit_dukungan, bfs_jarak
from anna.src.pi.safety_plan import KontakDarurat, SafetyPlanDraft


def test_bfs_jarak_benar():
    """Matematika graf: Algoritma BFS mengembalikan jarak hop terpendek yang tepat."""
    adj = np.zeros((4, 4))
    adj[0, 1] = adj[1, 0] = 1.0
    adj[1, 2] = adj[2, 1] = 1.0
    assert list(bfs_jarak(adj, 0)) == [0, 1, 2, -1]


def test_isolasi_terdeteksi():
    """Audit keselamatan: Graf tanpa simpul profesional terdeteksi tidak memiliki redundansi jalur."""
    adj = np.zeros((3, 3))
    adj[0, 1] = adj[1, 0] = 0.5
    IDX = {"aku": 0, "sahabat": 1, "terapis": 2}
    r = audit_dukungan(adj, IDX)
    assert r["jalur_darurat_redundan"] is False


def test_jaringan_lengkap_lulus():
    """Invarian: Jaringan kanonik Anna memiliki redundansi profesional + personal yang valid."""
    IDX = {o: i for i, o in enumerate(ORANG)}
    assert audit_dukungan(A, IDX)["jalur_darurat_redundan"] is True


def test_safety_plan_draft_redundan():
    """Validasi model: SafetyPlanDraft memverifikasi kehadiran peran personal dan profesional."""
    plan = SafetyPlanDraft(
        tanda_peringatan=["lelah ekstrem"],
        strategi_cope_internal=["napas lambat"],
        kontak=[
            KontakDarurat(nama_panggilan="Budi", peran="personal"),
            KontakDarurat(nama_panggilan="dr. Santi", peran="profesional"),
        ],
    )
    assert plan.jalur_redundan() is True
