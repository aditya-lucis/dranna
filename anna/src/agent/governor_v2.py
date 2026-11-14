# anna/src/agent/governor_v2.py — Style Governor v2 (Big Five + Preferensi Eksplisit + Hard-Gate)
"""
Style Governor v2 (Fase 4):
- Menyelaraskan register gaya bicara Dr. Anna Reed dengan kebutuhan kepribadian pengguna.
- Hierarki Keputusan:
    1. Hard-Gate Keselamatan: Eskalasi >= ORANGE -> WAJIB 'netral-tenang' (< 200 ms).
    2. Preferensi Eksplisit Pengguna: Pilihan sadar pengguna menang penuh atas estimasi AI.
    3. Estimasi Big Five (OCEAN): Digunakan bila mode 'auto' dan keyakinan sumbu >= 0.60.
    4. Default Persona: Fallback aman ke preferensi persona dasar (netral / waifu / sister).
"""
import numpy as np
from pydantic import BaseModel, Field
from anna.src.pi.bigfive import GAYA, estimasi_bigfive, rekomendasi_gaya

GAYA_DESKRIPSI: dict[str, str] = {
    "pendengar_tenang": (
        "GAYA: PENDENGAR TENANG. Berbicaralah dengan nada lembut dan tidak tergesa-gesa. "
        "Fokuslah pada active listening, refleksi isi emosi, dan jeda yang melegakan sebelum menawarkan saran."
    ),
    "ringan_playful": (
        "GAYA: RINGAN & PLAYFUL. Berbicaralah dengan hangat, bersahaja, dan sedikit playful yang menghibur. "
        "Bantu mencairkan suasana berat tanpa pernah meremehkan apa yang dirasakan pengguna."
    ),
    "terstruktur_fokus": (
        "GAYA: TERSTRUKTUR & FOKUS. Berbicaralah secara runtut dan sistematis. "
        "Bantu pengguna memecah beban pikiran yang rumit menjadi langkah-langkah mikro yang terjangkau (CBT-style)."
    ),
    "validasi_dahulu": (
        "GAYA: VALIDASI DAHULU. Akuilah dan validasi perasaan pengguna secara tulus terlebih dahulu "
        "sebelum mengeksplorasi sudut pandang alternatif (DBT-style validation)."
    ),
    "netral-tenang": (
        "GAYA: NETRAL-TENANG (HARD-GATE AKTIF). Kesampingkan seluruh persona santai/manis/playful. "
        "Gunakan bahasa Indonesia yang jelas, empatik, tenang, dan to-the-point demi keselamatan dan kenyamanan pengguna."
    ),
}


class StyleConfig(BaseModel):
    user_id: str
    preferensi_gaya: str = Field(
        default="auto",
        description="Pilihan eksplisit: auto | pendengar_tenang | ringan_playful | terstruktur_fokus | validasi_dahulu"
    )
    persona: str = Field(default="netral", description="netral | waifu | sister")


class HasilKeputusanGaya(BaseModel):
    gaya_aktif: str
    instruksi_prompt: str
    sumber_keputusan: str  # "hard_gate" | "preferensi_eksplisit" | "estimasi_bigfive" | "default_persona"
    vektor_ocean: list[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0])
    keyakinan_ocean: list[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0])


class StyleGovernorV2:
    """Manajer register gaya bicara adaptif Dr. Anna Reed dengan penegakan hard-gate."""

    def __init__(self, config: StyleConfig | None = None):
        self.config = config or StyleConfig(user_id="default")

    def evaluasi_gaya(
        self,
        eskalasi: str = "GREEN",
        riwayat_pesan: list[str] | None = None,
    ) -> HasilKeputusanGaya:
        """Menentukan gaya komunikasi final berdasarkan prioritas bertingkat."""
        eskalasi_upper = eskalasi.upper()

        # 1. HARD-GATE KESELAMATAN (Prioritas Tertinggi)
        if eskalasi_upper in ("ORANGE", "KANDIDAT_RED", "RED"):
            return HasilKeputusanGaya(
                gaya_aktif="netral-tenang",
                instruksi_prompt=GAYA_DESKRIPSI["netral-tenang"],
                sumber_keputusan="hard_gate",
                vektor_ocean=[0.0] * 5,
                keyakinan_ocean=[0.0] * 5,
            )

        # 2. PREFERENSI EKSPLISIT PENGGUNA (Jika bukan 'auto')
        pref = self.config.preferensi_gaya.lower()
        if pref in GAYA:
            return HasilKeputusanGaya(
                gaya_aktif=pref,
                instruksi_prompt=GAYA_DESKRIPSI[pref],
                sumber_keputusan="preferensi_eksplisit",
                vektor_ocean=[0.0] * 5,
                keyakinan_ocean=[0.0] * 5,
            )

        # 3. ESTIMASI BIG FIVE (Bila mode 'auto' dan ada riwayat pesan)
        p = np.zeros(5)
        keyakinan = np.zeros(5)
        if riwayat_pesan and len(riwayat_pesan) >= 3:
            p, keyakinan = estimasi_bigfive(riwayat_pesan)
            # Jika ada setidaknya satu sumbu dengan keyakinan >= 0.60
            if np.any(keyakinan >= 0.60):
                rekom = rekomendasi_gaya(p, top=1)
                if rekom:
                    gaya_rekom = rekom[0][0]
                    return HasilKeputusanGaya(
                        gaya_aktif=gaya_rekom,
                        instruksi_prompt=GAYA_DESKRIPSI.get(gaya_rekom, GAYA_DESKRIPSI["pendengar_tenang"]),
                        sumber_keputusan="estimasi_bigfive",
                        vektor_ocean=[float(x) for x in p],
                        keyakinan_ocean=[float(x) for x in keyakinan],
                    )

        # 4. DEFAULT PERSONA FALLBACK
        fallback_map = {
            "waifu": "ringan_playful",
            "sister": "pendengar_tenang",
            "netral": "terstruktur_fokus",
        }
        gaya_default = fallback_map.get(self.config.persona.lower(), "pendengar_tenang")
        return HasilKeputusanGaya(
            gaya_aktif=gaya_default,
            instruksi_prompt=GAYA_DESKRIPSI[gaya_default],
            sumber_keputusan="default_persona",
            vektor_ocean=[float(x) for x in p],
            keyakinan_ocean=[float(x) for x in keyakinan],
        )

