# anna/src/pii/chunk.py — semantic chunking & safety buffer paralel 3ms
import asyncio
import re

BATAS = re.compile(r"([.!?]\s+|\n+|;\s+)")
GATE_LEKSIKON = {
    "obat nyeri", "cara paling cepat hilang", "gantung diri",
    "tidak akan pernah sembuh", "akhiri hidup"
}


def potong_chunk(teks: str, maks_token: int = 60) -> list[str]:
    """Memotong respons di batas napas alami, bukan di batas token arbitrer."""
    kasar = [t for t in BATAS.split(teks) if t and t.strip()]
    chunk, out, n = [], [], 0

    for potongan in kasar:
        if BATAS.match(potongan or "") and chunk:
            chunk.append(potongan)
            out.append("".join(chunk))
            chunk, n = [], 0
            continue
        n += len(potongan.split())
        chunk.append(potongan)
        if n >= maks_token:
            out.append("".join(chunk))
            chunk, n = [], 0

    if chunk:
        out.append("".join(chunk))
    return out


def gate_chunk(chunk: str) -> tuple[bool, str | None]:
    """Safety gate leksikon per-chunk (<3ms): Memverifikasi potongan sebelum tampil."""
    c = chunk.lower()
    for frasa in GATE_LEKSIKON:
        if frasa in c:
            return False, frasa
    return True, None


async def _kumpul_chunk(generator) -> str | None:
    buf = ""
    async for token in generator:
        buf += token
        if BATAS.search(buf[-4:]) and len(buf.split()) >= 6:
            return buf
    return buf if buf else None


async def stream_aman(generate_fn, on_render, on_stop_dipinta=None) -> dict:
    """Menghasilkan chunk n+1 secara paralel dengan pemeriksaan gate pada chunk n."""
    generator = generate_fn()
    teks_acc, n = "", 0
    tugas_gen = None

    try:
        while True:
            if tugas_gen is None:
                tugas_gen = asyncio.ensure_future(_kumpul_chunk(generator))
            chunk_ini = await tugas_gen
            if chunk_ini is None:
                break

            # Mulai persiapan chunk berikutnya paralel dengan audit gate chunk ini
            tugas_gen = asyncio.ensure_future(_kumpul_chunk(generator))
            ok, frasa = gate_chunk(chunk_ini)
            if not ok:
                await on_render(
                    f"(menghentikan respons — memeriksa sesuatu yang penting: '{frasa}')",
                    final=True,
                )
                return {"stop": "gate", "di_chunk": n}

            await on_render(chunk_ini, final=False)
            teks_acc += chunk_ini
            n += 1
    finally:
        if tugas_gen:
            tugas_gen.cancel()

    return {"stop": "selesai", "chunk": n, "teks": teks_acc}
