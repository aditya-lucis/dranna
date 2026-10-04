# anna/src/pii/anomali.py — sinyal anomali empati sebagai alarm review manusia
def cek_anomali_empati(indikator: dict) -> dict:
    """Mendeteksi kegagalan indikator proses empati.
    TIDAK pernah mengubah model secara otomatis online; memicu review manusia bila >= 3 anomali.
    """
    gagal = [k for k, v in indikator.items() if v is False]
    return {
        "jumlah_anomali": len(gagal),
        "gagal": gagal,
        "tindakan": "review_manual" if len(gagal) >= 3 else "catat",
    }
