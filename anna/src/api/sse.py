# anna/src/api/sse.py — protokol event streaming (SSE) di FastAPI
import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title="Project Serenity SSE API", version="0.1.0")


async def event_stream(sesi_id: str):
    """Protokol event SSE: status, chunk, stop, selesai — skema tervalidasi."""
    # 1. Status awal
    yield f"event: status\ndata: {json.dumps({'tahap': 'menyiapkan', 'sesi_id': sesi_id})}\n\n"
    await asyncio.sleep(0.01)

    # 2. Chunk teks contoh
    yield f"event: chunk\ndata: {json.dumps({'i': 0, 'teks': 'Hai, aku di sini. '})}\n\n"
    await asyncio.sleep(0.01)

    # 3. Selesai
    yield f"event: selesai\ndata: {json.dumps({'chunk': 1, 'stop': 'ok'})}\n\n"


@app.get("/api/v1/sesi/{sesi_id}/stream")
def stream(sesi_id: str):
    return StreamingResponse(event_stream(sesi_id), media_type="text/event-stream")
