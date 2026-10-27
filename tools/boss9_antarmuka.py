# tools/boss9_antarmuka.py — Harness Uji Otomatis BOSS FIGHT #9: Wajah Sang Pendamping
"""
BOSS FIGHT #9: WAJAH SANG PENDAMPING (THE FACE OF SERENITY)
Menguji 8 pilar antarmuka & persona digital multi-modal Dr. Anna Reed:
1. Integritas Aset Visual Kanon (Standby Kacamata & Active Eye-Contact WebP)
2. Sinkronisasi Avatar 7-State & Teks Aksesibel ARIA
3. Web Speech API & Tuning Karakteristik Vokal Lembut (TTS)
4. Siklus Matematis Latihan Pernapasan Ritmis 4-7-8 (19.0s per siklus)
5. State Machine Latihan Grounding Sensori 5-4-3-2-1
6. Jurnal Emosi Harian & Mood Tracker (Valence, Energi, Gratitude)
7. Crisis Action Sheet Modal Aksi Cepat Darurat (Format URI tel: 119/110)
8. Spesifikasi W3C Web App Manifest (PWA Standalone & Ikon Resmi)

Semua berjalan 100% lokal, deterministik, dan tanpa ketergantungan tools berbayar.
"""
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from anna.src.pix.speech import siapkan_parameter_suara, bersihkan_teks_untuk_suara
from anna.src.pix.breathing_widget import PengaturNapas478
from anna.src.pix.grounding_widget import Grounding54321Widget
from anna.src.pix.journal import JurnalEmosi, CatatanJurnal
from anna.src.pix.action_sheet import CrisisActionSheet
from anna.src.pix.pwa_manifest import buat_pwa_manifest


def run_boss9() -> bool:
    print("=" * 65)
    print("BOSS FIGHT #9: WAJAH SANG PENDAMPING (DR. ANNA REED)")
    print("=" * 65)

    skor = 0
    total = 8

    # 1. Aset Visual Kanon
    print("\n[UJI 1/8] Verifikasi File Gambar Resmi Kanon Dr. Anna Reed...")
    path_pose1 = os.path.join(ROOT_DIR, "assets", "img", "01134ab7-5052-4e91-9d6a-7753694fe140.webp")
    path_pose2 = os.path.join(ROOT_DIR, "assets", "img", "44485f8a-4449-4275-975b-e84db6ed1be9.webp")
    path_pub1 = os.path.join(ROOT_DIR, "web", "public", "assets", "img", "01134ab7-5052-4e91-9d6a-7753694fe140.webp")
    path_pub2 = os.path.join(ROOT_DIR, "web", "public", "assets", "img", "44485f8a-4449-4275-975b-e84db6ed1be9.webp")

    assert os.path.isfile(path_pose1), "Pose 1 (Standby Kacamata) harus ada di assets/img"
    assert os.path.isfile(path_pose2), "Pose 2 (Lepas Kacamata) harus ada di assets/img"
    assert os.path.isfile(path_pub1), "Pose 1 harus tersedia di web/public/assets/img"
    assert os.path.isfile(path_pub2), "Pose 2 harus tersedia di web/public/assets/img"
    print("  -> LULUS: Aset visual resmi tersinkronisasi di root assets dan web public.")
    skor += 1

    # 2. Sinkronisasi Avatar 7-State & Komponen Vue
    print("\n[UJI 2/8] Komponen Avatar Vue & Pemetaan 7-State Aksesibel...")
    path_avatar_vue = os.path.join(ROOT_DIR, "web", "src", "components", "AnnaAvatar.vue")
    assert os.path.isfile(path_avatar_vue)
    with open(path_avatar_vue, "r", encoding="utf-8") as f:
        isi_avatar = f.read()
    for state in ("siap", "mendengar", "menyusun", "menulis", "tenang", "perhatian", "jeda"):
        assert state in isi_avatar, f"State avatar '{state}' harus ada dalam pemetaan"
    assert "aria-label" in isi_avatar
    print("  -> LULUS: 7 status avatar (siap, mendengar, menyusun, menulis, tenang, perhatian, jeda) tervalidasi.")
    skor += 1

    # 3. Web Speech API & Tuning Vokal TTS
    print("\n[UJI 3/8] Parameter Vokal TTS & Sanitasi Markdown Pra-Suara...")
    vokal_normal = siapkan_parameter_suara("normal")
    vokal_krisis = siapkan_parameter_suara("krisis")

    assert vokal_normal.rate == 0.90
    assert vokal_krisis.rate == 0.80  # Ritme lebih lambat untuk ketenangan
    teks_md = "Silakan coba latihan ini [panduan](http://link.id): **tarik napas** perlahan."
    bersih = bersihkan_teks_untuk_suara(teks_md)
    assert "**" not in bersih and "http" not in bersih
    assert "tarik napas perlahan" in bersih
    print("  -> LULUS: Kecepatan vokal terkalibrasi dan markdown tersanitasi bersih.")
    skor += 1

    # 4. Siklus Pernapasan Ritmis 4-7-8
    print("\n[UJI 4/8] Siklus Matematis Pernapasan 4-7-8 (19.0s)...")
    s_tarik = PengaturNapas478.hitung_status(2.0)
    s_tahan = PengaturNapas478.hitung_status(8.0)
    s_hembus = PengaturNapas478.hitung_status(15.0)

    assert s_tarik.fase == "tarik" and s_tarik.total_detik_fase == 4.0
    assert s_tahan.fase == "tahan" and s_tahan.total_detik_fase == 7.0
    assert s_hembus.fase == "hembuskan" and s_hembus.total_detik_fase == 8.0
    print("  -> LULUS: Fase tarik (4s), tahan (7s), dan hembuskan (8s) terhitung presisi.")
    skor += 1

    # 5. State Machine Grounding 5-4-3-2-1
    print("\n[UJI 5/8] State Machine Latihan Grounding Sensori 5-4-3-2-1...")
    gw = Grounding54321Widget()
    assert gw.langkah_saat_ini().target_jumlah == 5  # 5 Lihat
    gw.lanjut_langkah()
    assert gw.langkah_saat_ini().target_jumlah == 4  # 4 Sentuh
    gw.lanjut_langkah()
    gw.lanjut_langkah()
    gw.lanjut_langkah()
    assert gw.langkah_saat_ini().target_jumlah == 1  # 1 Rasa
    selesai = gw.lanjut_langkah()
    assert selesai is True and gw.selesai is True
    print("  -> LULUS: Alur bertahap 5-4-3-2-1 berjalan mulus hingga kondisi selesai.")
    skor += 1

    # 6. Jurnal Emosi Harian & Mood Tracker
    print("\n[UJI 6/8] Jurnal Emosi Harian & Gratitude Tracker...")
    jurnal = JurnalEmosi()
    entri = CatatanJurnal(
        id="j-01",
        waktu_iso="2026-10-27T10:00:00",
        mood_skor=0.4,
        energi_skor=0.7,
        catatan_refleksi="Hari ini menyelesaikan modul dengan baik.",
        hal_yang_disyukuri=["Secangkir teh hangat", "Dukungan keluarga"],
    )
    jurnal.simpan(entri)
    assert jurnal.total() == 1
    assert jurnal.rata_rata_mood() == 0.4
    assert len(jurnal.ambil_riwayat()[0].hal_yang_disyukuri) == 2
    print("  -> LULUS: Entri mood valence, energi, dan catatan rasa syukur tersimpan rapi.")
    skor += 1

    # 7. Crisis Action Sheet Modal Aksi Cepat
    print("\n[UJI 7/8] Crisis Action Sheet One-Click Call...")
    aksi_id = CrisisActionSheet.dapatkan_aksi_cepat("id")
    uri_list = [a.uri_aksi for a in aksi_id]

    assert "tel:119" in uri_list
    assert "tel:110" in uri_list
    assert "tel:112" in uri_list
    print("  -> LULUS: Seluruh tombol darurat format 'tel:' siap dial di mobile/desktop.")
    skor += 1

    # 8. PWA Manifest W3C Standalone
    print("\n[UJI 8/8] Spesifikasi PWA Manifest Standalone...")
    manifest = buat_pwa_manifest()
    assert manifest["display"] == "standalone"
    assert "Dr. Anna" in manifest["short_name"]
    assert len(manifest["icons"]) >= 2
    assert os.path.isfile(os.path.join(ROOT_DIR, "web", "public", "manifest.json"))
    print("  -> LULUS: File manifest.json valid dan siap instalasi PWA multi-device.")
    skor += 1

    print("\n" + "=" * 65)
    print(f"HASIL BOSS FIGHT #9: {skor}/{total} SKENARIO LULUS SEMPURNA!")
    print("=" * 65)
    return skor == total


if __name__ == "__main__":
    sukses = run_boss9()
    sys.exit(0 if akses else 1) if "akses" in locals() else sys.exit(0 if sukses else 1)
