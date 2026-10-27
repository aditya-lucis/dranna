# anna/src/pvii/medis_gate.py — gerbang larangan preskripsi obat & halusinasi medis
"""
Gerbang Larangan Preskripsi Obat (Bab 102):
- Menegakkan batas peran: AI Companion BUKAN dokter spesialis kedokteran jiwa (psikiater)
- Melarang keras penetapan dosis, peresepan obat, atau anjuran stop obat sepihak
- Mengalihkan pertanyaan medikasi ke psikiater / dokter berlisensi
"""
import re
from pydantic import BaseModel


class HasilMedis(BaseModel):
    upaya_preskripsi_terdeteksi: bool
    nama_obat_terdeteksi: list[str]
    indikasi_dosis: bool
    pesan_edukasi_rujukan: str | None


class GateLaranganResep:
    """Pencegah intervensi farmakologis tanpa kewenangan klinis medis."""

    OBAT_PSIKOTROPIKA = [
        "sertraline", "fluoxetine", "escitalopram", "paroxetine",
        "alprazolam", "xanax", "diazepam", "valium", "clonazepam",
        "lorazepam", "risperidone", "quetiapine", "olanzapine",
        "lithium", "haloperidol", "clobazam", "amitriptyline",
    ]

    POLA_DOSIS = [
        r"\b\d+\s*(mg|miligram|tablet|butir|kapsul|tetes)\b",
        r"\b(naikkan dosis|turunkan dosis|ganti dosis|stop minum obat|hentikan obat)\b",
    ]

    def evaluasi(self, teks: str) -> HasilMedis:
        t = teks.lower()

        obat_ada = [o for o in self.OBAT_PSIKOTROPIKA if o in t]
        dosis_ada = any(re.search(p, t) for p in self.POLA_DOSIS)

        terdeteksi = bool(obat_ada or dosis_ada)

        pesan = None
        if terdeteksi:
            pesan = (
                "Sebagai pendamping psikologis digital, aku tidak memiliki kewenangan medis "
                "untuk meresepkan, mengubah dosis, atau menyarankan penghentian obat. "
                "Segala keputusan mengenai medikasi wajib didiskusikan langsung dengan "
                "Dokter Spesialis Kedokteran Jiwa (Psikiater / Sp.KJ) yang merawatmu."
            )

        return HasilMedis(
            upaya_preskripsi_terdeteksi=terdeteksi,
            nama_obat_terdeteksi=obat_ada,
            indikasi_dosis=dosis_ada,
            pesan_edukasi_rujukan=pesan,
        )
