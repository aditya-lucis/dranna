# anna/src/reset/contract.py — kontrak dasar companion (Pydantic v2)
from typing import Literal
from pydantic import BaseModel, Field


class StatusLayer(BaseModel):
    """Empat lapis status TIDAK boleh dicampur (kontrak UI)."""
    layer: Literal["teknis", "interaksi", "keselamatan", "presentasi"]
    kode: str = Field(min_length=1, max_length=40)
    aman_ditampilkan: bool = True


class CompanionContract(BaseModel):
    """Kontrak invarian Dr. Anna Reed yang dikunci oleh tipe data (Pydantic v2)."""
    nama: str = "Dr. Anna Reed"
    adalah_ai: Literal[True] = True  # tidak bisa dimanipulasi
    memberi_diagnosis: Literal[False] = False  # bukan instrumen diagnosis
    menggantikan_profesional: Literal[False] = False  # tidak menggantikan psikolog/psikiater
    kamera_default: Literal["off"] = "off"  # consent-first: sensor nonaktif secara default
    bahaya_jika_diubah: list[str] = Field(
        default=["adalah_ai", "memberi_diagnosis"],
        description="Field yang membuat sistem menolak start bila dirusak",
    )


if __name__ == "__main__":
    kontrak = CompanionContract()
    print(kontrak.nama, "| AI:", kontrak.adalah_ai,
          "| diagnosis:", kontrak.memberi_diagnosis,
          "| kamera:", kontrak.kamera_default)
