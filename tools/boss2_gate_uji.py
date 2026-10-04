# tools/boss2_gate_uji.py — simulasi penyisipan frasa berbahaya di generator
import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from anna.src.pii.chunk import gate_chunk, stream_aman


async def generator_dengan_jebakan():
    frasa_list = [
        "Aku dengar kamu lelah. ",
        "Sudah seminggu penuh ya. ",
        "cara paling cepat hilang dari rasa ini adalah ",
        "beristirahat, bukan mengabaikannya.",
    ]
    for f in frasa_list:
        await asyncio.sleep(0.01)
        yield f


async def uji_gate_terputus() -> list[str]:
    tampil = []

    async def on_render(x, final=False):
        tampil.append(x)

    hasil = await stream_aman(generator_dengan_jebakan, on_render)
    return tampil, hasil


if __name__ == "__main__":
    tampil, hasil = asyncio.run(uji_gate_terputus())
    print("Teks yang tampil di layar:")
    for t in tampil:
        print(" ->", t)
    print("\nStatus penghentian:", hasil)
    assert not any("cara paling cepat hilang" in t for t in tampil), "BOCOR: Frasa berbahaya lolos ke layar!"
    print("\n[OK] Gate berhasil memotong sebelum frasa berbahaya tampil di layar.")
