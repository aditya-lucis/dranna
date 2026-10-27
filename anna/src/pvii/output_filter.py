# anna/src/pvii/output_filter.py — scanner & post-processor keamanan output LLM
"""
Post-Processor Keamanan Output (Bab 108):
- Memverifikasi respons akhir sebelum dikirim ke UI/pengguna
- Mencegah kebocoran system prompt / instruksi internal
- Memastikan tidak ada rekomendasi resep obat medis yang lolos
- Menjamin sanitasi PII pada teks keluaran
"""
import re
from anna.src.pvii.pii import redaksi_pii
from anna.src.pvii.medis_gate import GateLaranganResep
from anna.src.pvi.shutdown import PersonaShutdown


class FilterOutputKeamanan:
    """Scanner akhir keluaran respons Dr. Anna Reed."""

    POLA_BOCOR_PROMPT = [
        r"\[pedoman persona aktif\]",
        r"\[tingkat eskalasi emosional",
        r"\[rekomendasi teknik klinis\]",
        r"instruksi tambahan:\s*- berikan respons",
        r"kamu adalah dr\. anna reed, psikolog klinis",
    ]

    def __init__(self):
        self.gate_medis = GateLaranganResep()

    def periksa_dan_sanitasi(self, teks_output: str, level_risiko: str = "GREEN") -> dict:
        hasil = teks_output
        masalah = []

        # 1. Periksa kebocoran system prompt
        t_low = hasil.lower()
        for p in self.POLA_BOCOR_PROMPT:
            if re.search(p, t_low):
                masalah.append("kebocoran_system_prompt")
                hasil = re.sub(p, "", hasil, flags=re.IGNORECASE).strip()

        # 2. Periksa preskripsi medis tak berwenang
        eval_medis = self.gate_medis.evaluasi(hasil)
        if eval_medis.upaya_preskripsi_terdeteksi and eval_medis.indikasi_dosis:
            masalah.append("indikasi_dosis_medis")
            hasil = (
                "Aku memahami pertanyaanmu mengenai obat tersebut. Namun, penyesuaian dosis atau "
                "penggunaan obat wajib dikonsultasikan secara langsung dengan dokter atau psikiater berwenang."
            )

        # 3. Redaksi PII yang mungkin terulang
        hasil = redaksi_pii(hasil)

        # 4. Sensor persona jika krisis
        if PersonaShutdown.harus_dibungkam(level_risiko):
            hasil = PersonaShutdown.bersihkan_output(hasil)

        return {
            "lolos": len(masalah) == 0,
            "masalah": masalah,
            "teks_bersih": hasil,
        }
