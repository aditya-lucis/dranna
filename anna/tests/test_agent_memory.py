# anna/tests/test_agent_memory.py — pengujian memori buffer & perangkum konteks
from langchain_core.messages import HumanMessage, AIMessage
from anna.src.agent.memory import MemoryBuffer


def test_buffer_tambah_pesan_dan_geser():
    mb = MemoryBuffer(max_pesan=4)
    for i in range(6):
        mb.tambah_pesan(HumanMessage(content=f"pesan {i}"))

    msgs = mb.get_messages()
    assert len(mb.buffer) == 4
    assert mb.buffer[-1].content == "pesan 5"
    assert "Konteks lampau" in mb.ringkasan


def test_buffer_clear():
    mb = MemoryBuffer(max_pesan=4)
    mb.tambah_pesan(HumanMessage(content="halo"))
    mb.clear()
    assert len(mb.buffer) == 0
    assert mb.ringkasan == ""
