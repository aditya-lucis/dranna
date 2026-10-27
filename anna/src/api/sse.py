# anna/src/api/sse.py — protokol event streaming (SSE) di FastAPI terhubung ke LangGraph
import json
import asyncio
from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from anna.src.agent.streaming import stream_companion
from anna.src.agent.checkpoint import get_default_checkpointer
from anna.src.agent.graph import create_companion_graph

from anna.src.px.healthz import router_healthz

app = FastAPI(title="Project Serenity SSE API", version="1.0.0")
app.include_router(router_healthz)

# Checkpointer singleton untuk sesi
_checkpointer = get_default_checkpointer()
_graph = create_companion_graph(checkpointer=_checkpointer)


class ChatStreamRequest(BaseModel):
    pesan: str = Field(..., min_length=1, max_length=2000)
    persona: str = Field("netral", pattern="^(netral|waifu|sister)$")
    geo: str = Field("id", max_length=5)


@app.get("/api/v1/sesi/{sesi_id}/stream")
async def stream_get(
    sesi_id: str,
    pesan: str = Query("Halo Anna", description="Pesan dari pengguna"),
    persona: str = Query("netral", description="Persona: netral | waifu | sister"),
):
    """Streaming respons LangGraph Dr. Anna Reed via Server-Sent Events (GET)."""
    return StreamingResponse(
        stream_companion(
            pesan_pengguna=pesan,
            sesi_id=sesi_id,
            persona=persona,
            graph=_graph,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/v1/sesi/{sesi_id}/stream")
async def stream_post(
    sesi_id: str,
    req: ChatStreamRequest,
):
    """Streaming respons LangGraph Dr. Anna Reed via Server-Sent Events (POST)."""
    return StreamingResponse(
        stream_companion(
            pesan_pengguna=req.pesan,
            sesi_id=sesi_id,
            persona=req.persona,
            graph=_graph,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
