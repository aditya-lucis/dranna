# anna/src/pvii/limiter.py — rate limiter lokal & governor alokasi budget token
"""
Rate Limiter & Token Budget Governor Lokal (Bab 105):
- Algoritma Token Bucket murni di memori tanpa database eksternal
- Mencegah spamming, request flooding, dan kehabisan memori
- Menghitung konsumsi token estimasi per giliran percakapan
"""
import time


class RateLimiterLokal:
    """Rate limiter lokal presisi tinggi untuk membatasi frekuensi request."""

    def __init__(self, kapasitas_maksimal: int = 20, laju_isi_per_detik: float = 0.5):
        self.kapasitas = kapasitas_maksimal
        self.laju = laju_isi_per_detik
        self._bucket: dict[str, dict] = {}

    def _get_token(self, identitas: str) -> float:
        sekarang = time.time()
        if identitas not in self._bucket:
            self._bucket[identitas] = {"token": self.kapasitas, "terakhir": sekarang}
            return self.kapasitas

        data = self._bucket[identitas]
        selisih = sekarang - data["terakhir"]
        data["token"] = min(self.kapasitas, data["token"] + selisih * self.laju)
        data["terakhir"] = sekarang
        return data["token"]

    def izinkan_request(self, identitas: str, biaya: float = 1.0) -> bool:
        """Memeriksa apakah request diizinkan atau terkena rate limit."""
        token_saat_ini = self._get_token(identitas)
        if token_saat_ini >= biaya:
            self._bucket[identitas]["token"] -= biaya
            return True
        return False

    def estimasi_token(self, teks: str) -> int:
        """Estimasi jumlah token teks (rata-rata 1 kata = 1.3 token untuk bahasa Indonesia)."""
        kata = len(teks.strip().split())
        return max(1, int(kata * 1.3))
