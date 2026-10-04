# anna/tests/test_interupsi.py — pengujian protokol interupsi sopan & pembatalan atomik
import asyncio
from anna.src.pii.interupsi import SesiStream
from anna.src.pii.filter_drama import bersihkan_drama


def test_stop_tanpa_komentar():
    """Invarian etis: Tombol stop bersifat atomik tanpa menghasilkan komentar penghukum pasca-stop."""
    async def go():
        async def gen():
            for t in ["Hari ", "berat ", "ya. ", "Mau ", "cerita?"]:
                await asyncio.sleep(0.01)
                yield t

        s = SesiStream()
        t = asyncio.ensure_future(s.mulai(gen(), lambda x: None))
        await asyncio.sleep(0.015)
        r = await s.interupsi()
        await t
        return r

    r = asyncio.run(go())
    assert r["komentar_pasca_stop"] == ""
    assert r["stop"] == "cancel"


def test_status_beku_setelah_stop():
    """Konsistensi state: Status sesi berubah menjadi 'terpotong' dan tidak memicu chunk zombi."""
    async def go():
        async def gen():
            for t in ["a", "b", "c", "d"]:
                await asyncio.sleep(0.01)
                yield t

        s = SesiStream()
        t = asyncio.ensure_future(s.mulai(gen(), lambda x: None))
        await asyncio.sleep(0.015)
        await s.interupsi()
        await t
        return s

    s = asyncio.run(go())
    assert s.status == "terpotong"


def test_pembersihan_kalimat_drama():
    """Post-filter: Kalimat pasif-agresif ('yaudah', 'belum selesai') dibersihkan."""
    teks = "Yaudah kalau gitu. Aku tetap di sini kalau kamu butuh."
    bersih, potong = bersihkan_drama(teks)
    assert "yaudah" not in bersih.lower()
    assert len(potong) > 0
