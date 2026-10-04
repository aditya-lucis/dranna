# anna/src/pii/ui_bridge.py — jembatan event SSE status ke antarmuka aksesibel
def event_dari_status(lapis: str, pesan: str) -> dict:
    """Membentuk event SSE publik yang aman, terstandarisasi aria-live, dan ramah aksesibilitas."""
    return {
        "lapis": lapis,
        "pesan": pesan,
        "aria": f"status {lapis}: {pesan}",
        "warna_bukan_satu2nya": True,
    }
