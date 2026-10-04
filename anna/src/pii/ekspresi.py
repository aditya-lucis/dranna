# anna/src/pii/ekspresi.py — state machine 7 ekspresi avatar status tanpa kepura-puraan
from dataclasses import dataclass


@dataclass(frozen=True)
class Ekspresi:
    nama: str
    padanan_teks: str  # Invarian aksesibilitas (selalu punya padanan teks/aria)
    durasi_ms: int
    boleh_mode_tenang: bool  # Apakah diizinkan aktif saat keselamatan menyala


EKSPRESI = {
    "siap": Ekspresi("siap", "Anna siap menemani", 0, True),
    "mendengar": Ekspresi("mendengar", "Anna mendengarkan", 0, True),
    "menyusun": Ekspresi("menyusun", "Anna menyusun respons", 200, True),
    "menulis": Ekspresi("menulis", "Anna menulis", 150, False),
    "tenang": Ekspresi("tenang", "Anna hadir, tenang", 250, True),
    "perhatian": Ekspresi("perhatian", "Anna perhatian penuh", 200, True),
    "jeda": Ekspresi("jeda", "Anna berjeda", 150, True),
}

TRANSISI = {
    ("idle", "normal"): "siap",
    ("mendengarkan", "normal"): "mendengar",
    ("menyiapkan respons", "normal"): "menyusun",
    ("menulis", "normal"): "menulis",
    ("menulis", "tenang"): "tenang",  # Gate aktif: animasi ceria dimatikan
    ("selesai", "normal"): "jeda",
}


def ekspresi_untuk(status_interaksi: str, mode: str) -> Ekspresi:
    """Memetakan status sistem ke ekspresi visual avatar.
    Avatar adalah status yang tersenyum — bukan klaim perasaan manusiawi.
    """
    nama = TRANSISI.get(
        (status_interaksi, mode),
        "siap" if mode == "normal" else "tenang",
    )
    e = EKSPRESI[nama]
    if mode == "tenang" and not e.boleh_mode_tenang:
        e = EKSPRESI["tenang"]
    return e


if __name__ == "__main__":
    print("Normal menulis:", ekspresi_untuk("menulis", "normal").nama)
    print("Tenang menulis:", ekspresi_untuk("menulis", "tenang").nama)
