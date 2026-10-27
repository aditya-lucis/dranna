# anna/src/agent/memory.py — buffer memori geser & perangkum konteks percakapan
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage


class MemoryBuffer:
    """Manajer memori jendela geser dengan ringkasan otomatis saat percakapan panjang."""

    def __init__(self, max_pesan: int = 8):
        self.max_pesan = max_pesan
        self.ringkasan: str = ""
        self.buffer: list[BaseMessage] = []

    def tambah_pesan(self, pesan: BaseMessage | list[BaseMessage]):
        if isinstance(pesan, list):
            for p in pesan:
                self.tambah_pesan(p)
            return

        self.buffer.append(pesan)
        if len(self.buffer) > self.max_pesan:
            self._pangkas_dan_rangkum()

    def _pangkas_dan_rangkum(self):
        """Merangkum pesan tertua yang keluar dari jendela geser."""
        pesan_lama = self.buffer[:-self.max_pesan]
        self.buffer = self.buffer[-self.max_pesan:]

        poin_baru = []
        for p in pesan_lama:
            role = "Pengguna" if isinstance(p, HumanMessage) else "Anna"
            isi = p.content if isinstance(p.content, str) else str(p.content)
            poin_baru.append(f"{role}: {isi[:80]}")

        tambahan = "; ".join(poin_baru)
        if self.ringkasan:
            self.ringkasan = f"{self.ringkasan} | Konteks lampau: {tambahan}"
        else:
            self.ringkasan = f"Konteks lampau: {tambahan}"

        # Batasi panjang ringkasan agar tidak membengkak
        if len(self.ringkasan) > 800:
            self.ringkasan = self.ringkasan[-750:]

    def get_messages(self) -> list[BaseMessage]:
        """Mengembalikan pesan aktif, didahului oleh system message ringkasan jika ada."""
        hasil: list[BaseMessage] = []
        if self.ringkasan:
            hasil.append(SystemMessage(content=f"[Ringkasan Percakapan Sebelumnya: {self.ringkasan}]"))
        hasil.extend(self.buffer)
        return hasil

    def clear(self):
        self.buffer.clear()
        self.ringkasan = ""
