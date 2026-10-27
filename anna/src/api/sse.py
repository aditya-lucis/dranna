# anna/src/api/sse.py — protokol event streaming (SSE) di FastAPI terhubung ke LangGraph
import json
import os
from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from anna.src.agent.streaming import stream_companion
from anna.src.agent.checkpoint import get_default_checkpointer
from anna.src.agent.graph import create_companion_graph

from anna.src.px.healthz import router_healthz

app = FastAPI(title="Project Serenity SSE API", version="1.0.0")
app.include_router(router_healthz)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
WEB_DIR = os.path.join(ROOT_DIR, "web")

if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


@app.get("/", response_class=FileResponse)
def index_page():
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Dr. Anna Reed API active. Go to /docs for API documentation."}


@app.get("/manifest.json", response_class=FileResponse)
def pwa_manifest():
    manifest_path = os.path.join(WEB_DIR, "public", "manifest.json")
    if os.path.exists(manifest_path):
        return FileResponse(manifest_path, media_type="application/manifest+json")
    return {}

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
