# anna/src/pix/grounding_widget.py — state machine latihan sensori grounding 5-4-3-2-1
"""
State Tracker Latihan Grounding Sensori 5-4-3-2-1 (Bab 123):
- Langkah 1: 5 Hal yang DILIHAT
- Langkah 2: 4 Hal yang DISENTUH
- Langkah 3: 3 Hal yang DIDENGAR
- Langkah 4: 2 Hal yang DICIUM
- Langkah 5: 1 Hal yang DIRASAKAN (Cecapan / Lidah)
"""
from pydantic import BaseModel, Field


class LangkahGrounding(BaseModel):
    langkah: int = Field(ge=1, le=5)
    indra: str
    target_jumlah: int
    instruksi: str
    contoh: list[str]


class Grounding54321Widget:
    """Manajer alur latihan grounding somatik interaktif."""

    DAFTAR_LANGKAH: list[LangkahGrounding] = [
        LangkahGrounding(
            langkah=1,
            indra="Penglihatan",
            target_jumlah=5,
            instruksi="Sebutkan atau perhatikan 5 benda yang kamu LIHAT di sekitarmu saat ini.",
            contoh=["Layar komputer", "Buku di meja", "Warna dinding", "Jendela", "Bayangan lampu"],
        ),
        LangkahGrounding(
            langkah=2,
            indra="Sentuhan",
            target_jumlah=4,
            instruksi="Rasakan 4 hal yang bisa kamu SENTUH dengan tubuhmu.",
            contoh=["Kain bajumu", "Telapak kaki menyentuh lantai", "Permukaan meja", "Hembusan angin sepoi"],
        ),
        LangkahGrounding(
            langkah=3,
            indra="Pendengaran",
            target_jumlah=3,
            instruksi="Dengarkan dengan saksama 3 suara yang terdengar saat ini.",
            contoh=["Dengungan kipas/AC", "Suara kendaraan di kejauhan", "Suara napasmu sendiri"],
        ),
        LangkahGrounding(
            langkah=4,
            indra="Penciuman",
            target_jumlah=2,
            instruksi="Tarik napas dan kenali 2 aroma yang ada di sekitarmu.",
            contoh=["Aroma kopi/teh", "Wangi sabun atau udara ruangan"],
        ),
        LangkahGrounding(
            langkah=5,
            indra="Pengecapan",
            target_jumlah=1,
            instruksi="Sadarilah 1 rasa di lidah atau rongga mulutmu.",
            contoh=["Rasa air putih", "Sensasi segar udara di langit-langit mulut"],
        ),
    ]

    def __init__(self):
        self.indeks_aktif = 0
        self.selesai = False

    def langkah_saat_ini(self) -> LangkahGrounding:
        return self.DAFTAR_LANGKAH[self.indeks_aktif]

    def lanjut_langkah(self) -> bool:
        """Berpindah ke langkah berikutnya. Mengembalikan True jika sudah selesai seluruhnya."""
        if self.indeks_aktif < len(self.DAFTAR_LANGKAH) - 1:
            self.indeks_aktif += 1
            return False
        self.selesai = True
        return True

    def reset(self):
        self.indeks_aktif = 0
        self.selesai = False
