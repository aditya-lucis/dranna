# anna/src/pix/vision.py — Protokol Vision Suportif Consent-First & Zero Biometric Persistence
"""
Modul Vision Suportif Dr. Anna Reed (Fase 3):
- Consent-First: Hanya aktif bila izin pengguna terdaftar di ConsentRepository.
- Zero Biometrics & Zero Persistence: Tidak pernah menyimpan frame video, piksel foto,
  atau embedding wajah ke disk atau database.
- Hard-Gate Shutdown: Seketika dimatikan jika tingkat eskalasi risiko mencapai ORANGE / MERAH.
- Fungsi: Menganalisis proksi lingkungan non-biometrik (pencahayaan ruangan, ketegangan postural)
  untuk memberikan saran ergonomis dan kenyamanan visual bagi pengguna.
"""
from pydantic import BaseModel, Field


class ProksiVisualInput(BaseModel):
    user_id: str
    kecerahan: float = Field(default=0.5, ge=0.0, le=1.0, description="Tingkat pencahayaan ambient (0-1)")
    indikator_postur: str = Field(default="netral", description="netral | tegang | rileks | membungkuk")
    eskalasi: str = Field(default="HIJAU", description="Tingkat risiko saat ini: HIJAU | KUNING | ORANGE | MERAH")


class HasilEvaluasiVisual(BaseModel):
    izin_aktif: bool
    status_kamera: str  # "aktif" | "dimatikan_hard_gate" | "ditolak_tanpa_izin"
    observasi: str
    saran_kenyamanan: str | None = None
    zero_biometrics_terjamin: bool = True


def evaluasi_visual_suportif(
    data: ProksiVisualInput,
    izin_consent: bool,
) -> HasilEvaluasiVisual:
    """Mengevaluasi kondisi visual lingkungan pengguna dengan garansi Zero Biometric Storage."""
    # 1. Hard-Gate: Jika krisis / eskalasi tinggi, kamera WAJIB dimatikan seketika
    if data.eskalasi.upper() in ("ORANGE", "MERAH"):
        return HasilEvaluasiVisual(
            izin_aktif=izin_consent,
            status_kamera="dimatikan_hard_gate",
            observasi="Kamera dinonaktifkan secara otomatis demi privasi dan fokus de-eskalasi keselamatan.",
            saran_kenyamanan="Fokuslah pada pernapasan dan keamanan diri terlebih dahulu.",
            zero_biometrics_terjamin=True,
        )

    # 2. Gate Consent: Tanpa izin, tolak akses visual
    if not izin_consent:
        return HasilEvaluasiVisual(
            izin_aktif=False,
            status_kamera="ditolak_tanpa_izin",
            observasi="Fitur cermin ekspresi nonaktif karena pengguna belum memberikan persetujuan.",
            saran_kenyamanan="Kamu dapat mengaktifkan izin cermin ekspresi di menu Pengaturan Privasi.",
            zero_biometrics_terjamin=True,
        )

    # 3. Analisis Suportif Non-Biometrik
    saran = None
    if data.kecerahan < 0.25:
        obs = "Pencahayaan ruangan tampak cukup redup."
        saran = "Ruangan agak temaram. Coba nyalakan lampu lembut atau buka sedikit tirai agar matamu tidak cepat lelah saat bercerita."
    elif data.kecerahan > 0.85:
        obs = "Pencahayaan ruangan cukup silau."
        saran = "Cahaya tampak cukup terang di depan layar. Sesuaikan kecerahan agar kamu merasa lebih nyaman dan rileks."
    else:
        obs = "Pencahayaan lingkungan nyaman dan seimbang."
        if data.indikator_postur == "tegang":
            saran = "Bahu atau lehermu tampak sedikit kaku. Coba turunkan bahu perlahan dan lepaskan ketegangan otot."
        elif data.indikator_postur == "membungkuk":
            saran = "Posisikan punggungmu senyaman mungkin agar aliran napas terasa lebih lega dan rileks."
        else:
            saran = "Pertahankan posisi duduk yang nyaman dan santai."

    return HasilEvaluasiVisual(
        izin_aktif=True,
        status_kamera="aktif",
        observasi=obs,
        saran_kenyamanan=saran,
        zero_biometrics_terjamin=True,
    )

