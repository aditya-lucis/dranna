# anna/tests/test_agent_streaming.py — pengujian generator streaming SSE
import asyncio
from anna.src.agent.streaming import stream_companion
from anna.src.agent.graph import create_companion_graph
from anna.src.agent.provider import MockGeminiChat


def test_streaming_event_lengkap():
    graph = create_companion_graph(model=MockGeminiChat())

    async def run():
        events = []
        async for chunk in stream_companion("Halo Anna", graph=graph):
            events.append(chunk)
        return "".join(events)

    semua_event = asyncio.run(run())
    assert "event: status" in semua_event
    assert "event: chunk" in semua_event
    assert "event: reflection" in semua_event
    assert "event: selesai" in semua_event


def test_streaming_batal_instan():
    graph = create_companion_graph(model=MockGeminiChat())
    cancel_event = asyncio.Event()
    cancel_event.set()  # batalkan langsung

    async def run():
        events = []
        async for chunk in stream_companion("Halo Anna", graph=graph, cancel_event=cancel_event):
            events.append(chunk)
        return "".join(events)

    semua_event = asyncio.run(run())
    assert "dibatalkan" in semua_event
