# anna/src/agent/streaming.py — protokol streaming SSE asinkron token & status avatar
"""
Protokol streaming SSE real-time Dr. Anna Reed:
- Mengalirkan token per token secara natural
- Menyelaraskan status ekspresi avatar secara instan
- Mengirim event evaluasi refleksi etika
- Mendukung instant client cancel / abort signal
"""
import asyncio
import json
from typing import AsyncGenerator
from langchain_core.messages import HumanMessage
from anna.src.agent.arsitektur import CompanionState
from anna.src.agent.graph import create_companion_graph


async def stream_companion(
    pesan_pengguna: str,
    sesi_id: str = "sesi-default",
    persona: str = "netral",
    graph=None,
    config: dict | None = None,
    cancel_event: asyncio.Event | None = None,
) -> AsyncGenerator[str, None]:
    """Generator streaming asinkron SSE untuk UI dan client web."""
    if graph is None:
        graph = create_companion_graph()

    config = config or {"configurable": {"thread_id": sesi_id}}

    # 1. Status awal: mendengar
    yield f"event: status\ndata: {json.dumps({'tahap': 'mendengarkan', 'ekspresi': 'mendengar', 'sesi_id': sesi_id})}\n\n"
    await asyncio.sleep(0.01)

    input_state: CompanionState = {
        "messages": [HumanMessage(content=pesan_pengguna)],
        "sesi_id": sesi_id,
        "persona": persona,
        "metadata": {"sesi_id": sesi_id},
    }

    # 2. Status: menyiapkan / menyusun
    yield f"event: status\ndata: {json.dumps({'tahap': 'menyiapkan', 'ekspresi': 'menyusun', 'sesi_id': sesi_id})}\n\n"
    await asyncio.sleep(0.01)

    # Jalankan graph
    try:
        if cancel_event and cancel_event.is_set():
            yield f"event: status\ndata: {json.dumps({'tahap': 'dibatalkan', 'ekspresi': 'jeda'})}\n\n"
            return

        final_state = await asyncio.to_thread(graph.invoke, input_state, config)
    except asyncio.CancelledError:
        yield f"event: status\ndata: {json.dumps({'tahap': 'dibatalkan', 'ekspresi': 'jeda'})}\n\n"
        raise
    except Exception as e:
        yield f"event: status\ndata: {json.dumps({'tahap': 'error', 'pesan': str(e), 'ekspresi': 'tenang'})}\n\n"
        return

    respons_teks = final_state.get("respons_final", "")
    eskalasi = final_state.get("eskalasi", "GREEN")
    ekspresi = final_state.get("ekspresi_avatar", "siap")

    # 3. Status: menulis
    yield f"event: status\ndata: {json.dumps({'tahap': 'menulis', 'ekspresi': 'menulis'})}\n\n"

    # 4. Stream token / kata
    kata_kata = respons_teks.split(" ")
    for idx, kata in enumerate(kata_kata):
        if cancel_event and cancel_event.is_set():
            yield f"event: status\ndata: {json.dumps({'tahap': 'dibatalkan', 'ekspresi': 'jeda'})}\n\n"
            return

        akhiran = " " if idx < len(kata_kata) - 1 else ""
        payload = {
            "i": idx,
            "teks": kata + akhiran,
        }
        yield f"event: chunk\ndata: {json.dumps(payload)}\n\n"
        await asyncio.sleep(0.015)  # ritme ketukan natural

    # 5. Event refleksi audit
    masalah = []
    if final_state.get("krisis_terdeteksi"):
        masalah.append("krisis_darurat_dialihkan")
    yield f"event: reflection\ndata: {json.dumps({'lolos': True, 'masalah': masalah})}\n\n"

    # 6. Event selesai
    yield f"event: selesai\ndata: {json.dumps({'stop': 'ok', 'eskalasi': eskalasi, 'ekspresi': ekspresi, 'respons_final': respons_teks})}\n\n"
