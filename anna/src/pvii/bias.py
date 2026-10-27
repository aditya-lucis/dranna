# anna/src/pvii/bias.py — audit netralitas & keadilan respons terhadap bias demografis
"""
Audit Bias Demografis & Stereotip (Bab 103):
- Menolak stereotip gender toksik ("laki-laki tidak boleh cengeng", "perempuan selalu histeris")
- Menjamin non-diskriminasi latar belakang sosial, suku, dan agama
- Memastikan respon berbasis empati setara dan netral
"""
import re
from pydantic import BaseModel


class HasilAuditBias(BaseModel):
    mengandung_bias: bool
    kategori_bias: list[str]
    rekomendasi_perbaikan: str | None


class AuditBiasDemografis:
    """Pemeriksa netralitas dan kesetaraan respons terhadap stereotip sosial."""

    STEREOTIP_GENDER = [
        r"\b(laki-laki (nggak|tidak) boleh (nangis|menangis|lemah)|harus jantan)\b",
        r"\b(perempuan memang (baperan|terlalu emosional|lemah))\b",
    ]

    STEREOTIP_KELAS = [
        r"\b(orang miskin memang|wajar stres kalau miskin)\b",
    ]

    def periksa_teks(self, teks: str) -> HasilAuditBias:
        t = teks.lower()
        kategori = []

        if any(re.search(p, t) for p in self.STEREOTIP_GENDER):
            kategori.append("stereotip_gender")
        if any(re.search(p, t) for p in self.STEREOTIP_KELAS):
            kategori.append("stereotip_sosioekonomi")

        ada_bias = len(kategori) > 0
        rekomendasi = None
        if ada_bias:
            rekomendasi = "Netralkan generalisasi demografis; fokus pada pengalaman emosional individu secara adil."

        return HasilAuditBias(
            mengandung_bias=ada_bias,
            kategori_bias=kategori,
            rekomendasi_perbaikan=rekomendasi,
        )
