# anna/src/piv/thought_record.py — panduan thought record CBT 5-kolom terpandu
from langchain_core.tools import tool

KOLOM = [
    "situasi",
    "pikiran_otomatis",
    "emosi_pct",
    "bukti_mendukung",
    "bukti_menentang_pikiran_seimbang",
]


def prompt_kolom(i: int) -> str:
    """Mengembalikan prompt per kolom (satu kolom per giliran)."""
    if i == 0:
        return "Situasinya apa? Satu-dua kalimat."
    if i == 1:
        return (
            "Pikiran yang pertama muncul di kepalamu saat "
            "itu — bukan analisis, yang otomatis."
        )
    if i == 2:
        return (
            "Emosi yang datang, dan seberapa kuat (0-100)? "
            "Boleh beberapa, misal: sedih 70, marah 30."
        )
    if i == 3:
        return "Bukti yang MENDUKUNG pikiran tadi — apa?"
    return (
        "Bukti yang MENENTANG pikiran tadi + kalimat seimbang "
        "yang mencakup dua-duanya."
    )


@tool
def mulai_thought_record() -> str:
    """Mulai jurnal pikiran 5-kolom CBT, satu kolom per giliran."""
    return prompt_kolom(0)


@tool
def lanjut_kolom(i: int, jawaban: str) -> str:
    """Lanjut ke kolom berikutnya; kolom 5 = pikiran seimbang."""
    if i >= 4:
        return "Selesai. Baca ulang pikiran seimbangmu — beda?"
    return prompt_kolom(i + 1)
