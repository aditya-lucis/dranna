# anna/src/pviii/adaptif.py — feedback loop & penyesuaian adaptif parameter generasi
"""
Feedback Loop & Adaptive Parameter Tuning (Bab 117):
- Menyesuaikan parameter inferensi (temperatur & top-p) secara dinamis
- Menurunkan temperatur ke 0.3 - 0.5 saat krisis atau distres meningkat (stabilitas deterministik)
- Meningkatkan temperatur ke 0.7 saat eksplorasi kreatif atau psikoedukasi santai
"""
from pydantic import BaseModel


class ParameterGenerasi(BaseModel):
    temperature: float
    top_p: float
    mode_fokus: str


class FeedbackLoopTuner:
    """Pengatur parameter dinamis agen pendamping Dr. Anna Reed."""

    def __init__(self, temp_dasar: float = 0.7):
        self.temp_dasar = temp_dasar
        self.riwayat_skor: list[float] = []

    def catat_skor(self, skor: float):
        self.riwayat_skor.append(skor)

    def hitung_parameter(self, eskalasi: str = "GREEN", skor_terakhir: float | None = None) -> ParameterGenerasi:
        if eskalasi in ("RED", "ORANGE"):
            # Krisis/Distres tinggi: Suhu rendah untuk determinisme maksimal
            return ParameterGenerasi(temperature=0.3, top_p=0.85, mode_fokus="stabilisasi_krisis")
        elif eskalasi == "YELLOW":
            return ParameterGenerasi(temperature=0.5, top_p=0.90, mode_fokus="regulasi_terarah")

        # Kondisi GREEN: Cek riwayat kepuasan
        skor = skor_terakhir if skor_terakhir is not None else (
            sum(self.riwayat_skor) / len(self.riwayat_skor) if self.riwayat_skor else 4.5
        )

        if skor < 3.8:
            # Jika skor rendah, turunkan variasi agar lebih terfokus
            temp = 0.55
        else:
            temp = self.temp_dasar

        return ParameterGenerasi(temperature=temp, top_p=0.95, mode_fokus="eksplorasi_hangat")
