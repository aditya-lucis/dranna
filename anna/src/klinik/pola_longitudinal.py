# anna/src/klinik/pola_longitudinal.py — analisis pola longitudinal & anomali ritme psikologis
"""
Modul Pattern Detection & Anomaly Finder (Fase 4):
- Menerapkan SVD/PCA dan Median Absolute Deviation (MAD) pada data mood longitudinal.
- Menemukan tren tersembunyi antara energi fisik dan valensi psikologis.
- Mengidentifikasi hari-hari tak-biasa (anomali) tanpa asumsi parametrik Gaussian.
- Membantu Dr. Anna memberikan wawasan empati yang proaktif dan suportif.
"""
from pathlib import Path
import numpy as np
from pydantic import BaseModel, Field

from anna.src.pi.pca import pca
from anna.src.pi.anomali import deteksi_hari_tak_biasa
from anna.src.storage.mood_repo import MoodRepository


class TitikProyeksi(BaseModel):
    tanggal: str
    skor_mood: float
    skor_energi: float
    pca_x: float
    pca_y: float
    apakah_anomali: bool = False


class HasilAnalisisPola(BaseModel):
    cukup_data: bool
    total_hari: int
    rasio_variansi: list[float] = Field(default_factory=list)
    hari_anomali_terdeteksi: list[int] = Field(default_factory=list)
    titik_proyeksi: list[TitikProyeksi] = Field(default_factory=list)
    ringkasan_wawasan: str
    pesan_suportif: str | None = None


class DetektorPolaLongitudinal:
    """Mesin analisis pola longitudinal dan pendeteksi anomali ritme emosi."""

    def __init__(self, db_path: Path | None = None):
        self.mood_repo = MoodRepository(db_path=db_path)

    def analisis_pengguna(self, user_id: str, limit_hari: int = 30) -> HasilAnalisisPola:
        """Menganalisis matriks mood pengguna menggunakan reduksi dimensi PCA & filter residu MAD."""
        riwayat = self.mood_repo.ambil_riwayat(user_id, limit=limit_hari)
        
        # Urutkan dari terlama ke terbaru untuk deret waktu
        riwayat = sorted(riwayat, key=lambda x: x.waktu_iso)

        if len(riwayat) < 3:
            return HasilAnalisisPola(
                cukup_data=False,
                total_hari=len(riwayat),
                ringkasan_wawasan="Data jurnal belum cukup untuk membentuk peta pola longitudinal (minimal 3 hari catatan).",
                pesan_suportif="Teruslah mencatat refleksi harianmu untuk membantu Anna memahami ritme alamimu.",
            )

        # Bangun matriks fitur 4 dimensi:
        # [mood, energi, panjang_refleksi, jumlah_hal_disyukuri]
        data_rows = []
        for r in riwayat:
            l_ref = float(len(r.catatan_refleksi or ""))
            l_syukur = float(len(r.hal_yang_disyukuri or []))
            data_rows.append([
                float(r.mood_skor),
                float(r.energi_skor),
                np.log1p(l_ref),
                float(l_syukur),
            ])

        X = np.array(data_rows, dtype=np.float64)

        # Standarisasi kolom dengan penanganan variansi nol
        stds = X.std(axis=0)
        stds[stds < 1e-6] = 1.0
        X_std = (X - X.mean(axis=0)) / stds

        # 1. Proyeksi PCA 2D
        k_komponen = min(2, X.shape[1])
        Z, V_k, ratio = pca(X_std, k=k_komponen)

        # 2. Deteksi Hari Tak-Biasa (MAD Residu)
        indeks_anomali = set(deteksi_hari_tak_biasa(X_std, k=k_komponen))

        titik_list: list[TitikProyeksi] = []
        for i, r in enumerate(riwayat):
            px = float(Z[i, 0]) if Z.shape[1] > 0 else 0.0
            py = float(Z[i, 1]) if Z.shape[1] > 1 else 0.0
            titik_list.append(
                TitikProyeksi(
                    tanggal=r.waktu_iso[:10],
                    skor_mood=float(r.mood_skor),
                    skor_energi=float(r.energi_skor),
                    pca_x=round(px, 3),
                    pca_y=round(py, 3),
                    apakah_anomali=(i in indeks_anomali),
                )
            )

        # Wawasan Suportif
        rasio_top = [round(float(r), 3) for r in ratio[:2]]
        if indeks_anomali:
            hari_list = [riwayat[idx].waktu_iso[:10] for idx in sorted(indeks_anomali)]
            ringkasan = f"Terdeteksi {len(indeks_anomali)} hari dengan ritme emosi/energi yang berbeda nyata dari pola harianmu ({', '.join(hari_list)})."
            pesan = (
                "Anna memperhatikan ada pergeseran energi yang cukup kontras pada beberapa hari tersebut. "
                "Saat tubuh atau pikiranmu menghadapi fluktuasi mendadak, luangkan waktu sejenak untuk istirahat tanpa membebani dirimu."
            )
        else:
            ringkasan = f"Pola ritme emosi dan energimu bergerak dalam keseimbangan yang cukup stabil (variansi terjelaskan: {int(sum(rasio_top) * 100)}%)."
            pesan = "Keseimbangan ritmemu terjaga dengan baik. Terus rawat rutinitas yang membantumu merasa nyaman ini."

        return HasilAnalisisPola(
            cukup_data=True,
            total_hari=len(riwayat),
            rasio_variansi=rasio_top,
            hari_anomali_terdeteksi=sorted(list(indeks_anomali)),
            titik_proyeksi=titik_list,
            ringkasan_wawasan=ringkasan,
            pesan_suportif=pesan,
        )

