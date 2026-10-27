# anna/src/agent/checkpoint.py — checkpointing sesi percakapan & persistensi pulih
"""
Sistem manajemen sesi dan checkpointing LangGraph 1.2:
- Menyimpan snapshot state per thread/sesi
- Pulih dari interupsi atau kegagalan koneksi
- Memungkinkan time-travel / rollback riwayat jika diperlukan
"""
from typing import Any
from langgraph.checkpoint.memory import MemorySaver


class SessionCheckpointManager:
    """Pengelola checkpointer state sesi percakapan Anna."""

    def __init__(self, checkpointer: Any | None = None):
        self.checkpointer = checkpointer or MemorySaver()
        self._active_sessions: dict[str, dict] = {}

    def get_checkpointer(self):
        return self.checkpointer

    def catat_sesi(self, sesi_id: str, metadata: dict | None = None):
        self._active_sessions[sesi_id] = {
            "sesi_id": sesi_id,
            "metadata": metadata or {},
        }

    def get_sesi(self, sesi_id: str) -> dict | None:
        return self._active_sessions.get(sesi_id)

    def hapus_sesi(self, sesi_id: str):
        if sesi_id in self._active_sessions:
            del self._active_sessions[sesi_id]


_GLOBAL_CHECKPOINTER = None


def get_default_checkpointer() -> MemorySaver:
    global _GLOBAL_CHECKPOINTER
    if _GLOBAL_CHECKPOINTER is None:
        _GLOBAL_CHECKPOINTER = MemorySaver()
    return _GLOBAL_CHECKPOINTER
