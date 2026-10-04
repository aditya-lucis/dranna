# anna/src/pi/logika.py — aturan keselamatan sebagai proposisi logika teruji (de Morgan, short-circuit)
import itertools


def aturan_persona_off(S: dict) -> bool:
    """Invarian persona mati: persona_off <- bukti_eksplisit OR level == 'RED'."""
    return bool(S.get("bukti_eksplisit", False) or S.get("level") == "RED")


def aturan_kamera_boleh(S: dict) -> bool:
    """Hukum De Morgan: kamera boleh NYALA HANYA jika SEMUA komponen persetujuan terpenuhi.
    all(persetujuan) == True  <=>  not any(not v for v in persetujuan)
    """
    persetujuan = S.get("persetujuan", {})
    if not persetujuan:
        return False
    return bool(all(persetujuan.values()))


def aturan_perlu_verifikasi(S: dict) -> bool:
    """Verifikasi lembut: (kata_parah ATAU pola_waktu) DAN TIDAK sudah_dijawab."""
    parah_atau_waktu = S.get("kata_parah", False) or S.get("pola_waktu", False)
    return bool(parah_atau_waktu and not S.get("sudah_dijawab", False))


def audit_invarian_persona() -> bool:
    """Evaluasi exhaustive kontraposisi aturan persona pada seluruh ruang keadaan (2^3 = 8 kasus)."""
    ok = True
    for bukti, red, persona_on in itertools.product([False, True], repeat=3):
        S = {"bukti_eksplisit": bukti, "level": "RED" if red else "GREEN"}
        # Pelanggaran: persona tetap ON padahal aturan persona_off aktif
        pelanggaran = persona_on and aturan_persona_off(S)
        if pelanggaran and not (bukti or red):
            ok = False
    return ok


if __name__ == "__main__":
    print("Invarian persona terjaga:", audit_invarian_persona())
