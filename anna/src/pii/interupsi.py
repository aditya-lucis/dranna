# anna/src/pii/interupsi.py — protokol interupsi atomik & resume tanpa rasa bersalah
import asyncio


class SesiStream:
    """Mengelola siklus streaming yang dapat dihentikan kapan saja secara atomik."""

    def __init__(self):
        self.tugas_gen = None
        self.teks_tampil = ""
        self.status = "idle"  # idle | menulis | terpotong | selesai

    async def mulai(self, generator, on_render):
        self.status = "menulis"
        self.tugas_gen = asyncio.ensure_future(self._gen(generator, on_render))
        return await self.tugas_gen

    async def _gen(self, generator, on_render):
        try:
            async for token in generator:
                if self.status == "terpotong":
                    break
                self.teks_tampil += token
                if callable(on_render):
                    res = on_render(token)
                    if asyncio.iscoroutine(res):
                        await res
            self.status = "selesai"
            return {"teks": self.teks_tampil, "stop": "natural"}
        except asyncio.CancelledError:
            return {"teks": self.teks_tampil, "stop": "cancel"}

    async def interupsi(self) -> dict:
        """STOP atomik: membatalkan coroutine, membekukan teks, dan tanpa komentar penghukum."""
        if self.tugas_gen and not self.tugas_gen.done():
            self.tugas_gen.cancel()
        self.status = "terpotong"
        return {
            "teks": self.teks_tampil,
            "titik_potong": len(self.teks_tampil),
            "komentar_pasca_stop": "",  # Wajib selalu kosong by design
            "stop": "cancel",
        }

    async def lanjut(self, generator, on_render):
        """Resume DARI titik potong tanpa mengulang kalimat dari awal."""
        sudah = len(self.teks_tampil)
        self.status = "menulis"
        self.tugas_gen = asyncio.ensure_future(
            self._gen_lanjut(generator, on_render, sudah)
        )
        return await self.tugas_gen

    async def _gen_lanjut(self, generator, on_render, sudah):
        async for token in generator:
            self.teks_tampil += token
            if callable(on_render):
                res = on_render(token)
                if asyncio.iscoroutine(res):
                    await res
        self.status = "selesai"
        return {"teks": self.teks_tampil, "stop": "natural"}
