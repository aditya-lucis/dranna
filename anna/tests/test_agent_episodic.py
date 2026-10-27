# anna/tests/test_agent_episodic.py — pengujian memori episodik & pencarian kosinus
import numpy as np
from anna.src.agent.episodic import Episode, EpisodicStore


def test_episodic_simpan_dan_cari():
    store = EpisodicStore()
    v1 = [1.0, 0.0, 0.0, 0.0]
    v2 = [0.0, 1.0, 0.0, 0.0]

    ep1 = Episode(
        id="ep-1",
        sesi_id="sesi-1",
        waktu="2026-10-21T10:00:00",
        topik="panik",
        valence=-0.6,
        arousal=0.8,
        teknik_dipakai="breathing_478",
        hasil_respon="positif",
        embed=v1,
    )
    ep2 = Episode(
        id="ep-2",
        sesi_id="sesi-2",
        waktu="2026-10-21T11:00:00",
        topik="burnout",
        valence=-0.4,
        arousal=0.3,
        teknik_dipakai="restrukturisasi",
        hasil_respon="netral",
        embed=v2,
    )

    store.simpan_episode(ep1)
    store.simpan_episode(ep2)

    assert store.total() == 2

    # Cari serupa dengan v1
    hasil = store.cari_serupa(query_embed=np.array(v1, dtype=float), ambang_kosinus=0.8)
    assert len(hasil) == 1
    assert hasil[0]["episode"].id == "ep-1"
    assert hasil[0]["kosinus"] >= 0.99
