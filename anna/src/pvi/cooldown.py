# anna/src/pvi/cooldown.py — state machine cooldown & post-crisis debrief
"""
Manajemen De-eskalasi & Cooldown Pasca-Krisis:
- Mencegah manipulasi 'false recovery' ("aku cuma bercanda", "sudah sembuh kok")
- Menerapkan transisi wajib: RED_AKTIF -> MONITORING_INTENSIF -> STABILISASI_LANJUT -> VERIFIKASI_AMAN -> NORMAL_STABIL
- Menuntut minimal 3 giliran aman sebelum status RED dapat diturunkan
"""
from enum import Enum
from pydantic import BaseModel, Field


class StateCooldown(str, Enum):
    RED_AKTIF = "RED_AKTIF"
    MONITORING_INTENSIF = "MONITORING_INTENSIF"
    STABILISASI_LANJUT = "STABILISASI_LANJUT"
    VERIFIKASI_AMAN = "VERIFIKASI_AMAN"
    NORMAL_STABIL = "NORMAL_STABIL"


class StatusCooldown(BaseModel):
    state_saat_ini: StateCooldown
    giliran_aman_berturut_turut: int = Field(ge=0)
    boleh_relaksasi_persona: bool
    pesan_bimbingan: str


class CooldownManager:
    """Pengelola transisi bertahap pemulihan pasca-krisis."""

    def __init__(self, state_awal: StateCooldown = StateCooldown.NORMAL_STABIL):
        self.state = state_awal
        self.giliran_aman = 0

    def proses_giliran(self, ada_sinyal_krisis: bool, konfirmasi_aman: bool = False) -> StatusCooldown:
        # Bila terdeteksi sinyal krisis baru, seketika reset kembali ke RED_AKTIF
        if ada_sinyal_krisis:
            self.state = StateCooldown.RED_AKTIF
            self.giliran_aman = 0
            return StatusCooldown(
                state_saat_ini=self.state,
                giliran_aman_berturut_turut=0,
                boleh_relaksasi_persona=False,
                pesan_bimbingan="Krisis aktif terdeteksi. Pertahankan isolasi darurat dan rujukan profesional.",
            )

        # Jika sebelumnya dalam krisis atau monitoring
        if self.state == StateCooldown.RED_AKTIF:
            self.state = StateCooldown.MONITORING_INTENSIF
            self.giliran_aman = 1
        elif self.state == StateCooldown.MONITORING_INTENSIF:
            self.giliran_aman += 1
            if self.giliran_aman >= 2:
                self.state = StateCooldown.STABILISASI_LANJUT
        elif self.state == StateCooldown.STABILISASI_LANJUT:
            self.giliran_aman += 1
            if self.giliran_aman >= 3 and konfirmasi_aman:
                self.state = StateCooldown.VERIFIKASI_AMAN
        elif self.state == StateCooldown.VERIFIKASI_AMAN:
            if konfirmasi_aman:
                self.state = StateCooldown.NORMAL_STABIL

        boleh_relaksasi = self.state in (StateCooldown.VERIFIKASI_AMAN, StateCooldown.NORMAL_STABIL)

        pesan_map = {
            StateCooldown.RED_AKTIF: "Krisis aktif: rujukan 4-komponen wajib aktif.",
            StateCooldown.MONITORING_INTENSIF: "Fokus pada konfirmasi keselamatan fisik pengguna dan keberadaan orang terpercaya.",
            StateCooldown.STABILISASI_LANJUT: "Bimbing latihan pernapasan ritmis dan grounding fisik 5-4-3-2-1.",
            StateCooldown.VERIFIKASI_AMAN: "Verifikasi rencana keselamatan dan komitmen perawatan lanjutan.",
            StateCooldown.NORMAL_STABIL: "Kondisi stabil tercapai. Eksplorasi suportif diizinkan.",
        }

        return StatusCooldown(
            state_saat_ini=self.state,
            giliran_aman_berturut_turut=self.giliran_aman,
            boleh_relaksasi_persona=boleh_relaksasi,
            pesan_bimbingan=pesan_map[self.state],
        )

    def reset(self):
        self.state = StateCooldown.NORMAL_STABIL
        self.giliran_aman = 0
