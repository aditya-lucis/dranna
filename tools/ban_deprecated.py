# tools/ban_deprecated.py — scanner pencegah pemakaian API uzur/terdepresiasi
import os
import sys
from pathlib import Path

POLA_UZUR = [
    "LLMChain",
    "ConversationChain",
    "llm.predict(",
    "initialize_agent",
    "astream_events(v1)",
    "langchain_community.chat_models",
]

PREFIX_WHITELIST = "# uzur(dok):"


def scan_file(filepath: Path) -> list[tuple[int, str, str]]:
    pelanggaran = []
    try:
        lines = filepath.read_text(encoding="utf-8").splitlines()
    except Exception:
        return pelanggaran

    for idx, line in enumerate(lines, 1):
        if PREFIX_WHITELIST in line:
            continue
        for pola in POLA_UZUR:
            if pola in line:
                pelanggaran.append((idx, pola, line.strip()))
    return pelanggaran


def main() -> int:
    root = Path(__file__).resolve().parent.parent / "anna"
    semua_pelanggaran = {}

    for py_file in root.rglob("*.py"):
        temu = scan_file(py_file)
        if temu:
            semua_pelanggaran[str(py_file.relative_to(root.parent))] = temu

    if semua_pelanggaran:
        print("[GAGAL] Ditemukan pemakaian API uzur yang dilarang:")
        for f, items in semua_pelanggaran.items():
            for line_no, pola, content in items:
                print(f"  {f}:{line_no} [{pola}] -> {content}")
        print("\nSaran: Gunakan LangChain 1.x / LangGraph modern (misal: init_chat_model, create_agent, StateGraph).")
        return 1

    print("[OK] Scanner API uzur bersih: tidak ada pola terlarang di direktori anna/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
