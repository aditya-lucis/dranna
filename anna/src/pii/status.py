# anna/src/pii/status.py — sistem 4 lapis status interaksi independen dengan hierarki prioritas
from enum import StrEnum
from dataclasses import dataclass


class Teknis(StrEnum):
    TERHUBUNG = "terhubung"
    BUFFERING = "buffering"
    TIMEOUT = "timeout"
    RETRY = "retry"
    GAGAL = "gagal"
    TERSIMPAN_OFFLINE = "tersimpan-offline"


class Interaksi(StrEnum):
    MENDENGARKAN = "mendengarkan"
    MENYIAPKAN = "menyiapkan respons"
    MENULIS = "menulis"
    MENYEIMBANGKAN = "jeda disengaja"
    MENGETIK_LAMA = "mengetik-lama"
    SELESAI = "selesai"


class Keselamatan(StrEnum):
    MEMERIKSA = "memeriksa keselamatan respons"
    PENTING = "ada hal penting"
    MENGALIHKAN = "mengalihkan ke bantuan manusia"


@dataclass
class StatusBertingkat:
    """Mengelola status sistem bertingkat tanpa pencampuran lapis.
    Prioritas mutlak: Keselamatan > Teknis > Interaksi > Presentasi.
    """
    teknis: Teknis = Teknis.TERHUBUNG
    interaksi: Interaksi | None = None
    keselamatan: Keselamatan | None = None
    presentasi_mode: str = "normal"  # normal | tenang | reduced

    def tampil(self) -> tuple[str, str]:
        """Mengembalikan pasangan (lapisan_aktif, deskripsi_pesan)."""
        if self.keselamatan:
            self.presentasi_mode = "tenang"  # Kontrak etis, bukan sekadar gaya
            return ("keselamatan", str(self.keselamatan.value if hasattr(self.keselamatan, "value") else self.keselamatan))

        if self.teknis in (Teknis.GAGAL, Teknis.RETRY, Teknis.TIMEOUT, Teknis.TERSIMPAN_OFFLINE):
            return ("teknis", f"{self.teknis} — jujur soal teknis")

        if self.interaksi:
            return ("interaksi", str(self.interaksi.value if hasattr(self.interaksi, "value") else self.interaksi))

        return ("presentasi", self.presentasi_mode)
