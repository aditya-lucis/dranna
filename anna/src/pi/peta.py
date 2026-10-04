# anna/src/pi/peta.py — cabang psikologi sebagai dependensi berbobot
import numpy as np

CABANG = np.array([
    # keandalan_bukti, boleh_memutuskan (0/1)
    [0.90, 0],  # klinis: sangat terukur, tapi TIDAK memutuskan (rujuk manusia)
    [0.80, 1],  # kognitif: terukur, boleh memutuskan desain respons
    [0.55, 0],  # perkembangan: deskriptif, hanya inspirasi
    [0.60, 1],  # kepribadian: cukup stabil utk personalisasi ringan
    [0.65, 1],  # sosial-positif: kerangka refleksi
])

NAMA = ["klinis", "kognitif", "perkembangan", "kepribadian", "sosial+"]


def bobot_prioritas() -> dict:
    """Makin andal buktinya, makin besar suaranya.
    Yang tanpa izin memutuskan hanya boleh mewarnai, bukan menyetir.
    """
    w = CABANG[:, 0] / CABANG[:, 0].sum()
    return {
        n: (round(float(wi), 3), bool(b))
        for n, wi, b in zip(NAMA, w, CABANG[:, 1])
    }


if __name__ == "__main__":
    print(bobot_prioritas())
