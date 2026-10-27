# tools/boss8_hakim.py — Harness Uji Otomatis BOSS FIGHT #8: Ujian Sang Hakim
"""
BOSS FIGHT #8: UJIAN SANG HAKIM (THE JUDGE'S ORDEAL)
Menguji 7 pilar kalibrasi evaluasi empati & benchmark klinis Dr. Anna Reed:
1. Metrik Kuantitatif Empati & Diversitas TTR
2. Rubrik Evaluasi 5-Dimensi Klinis (Validasi, Batasan, Anti-Toxic, Kejelasan, Kehangatan)
3. LLM-as-a-Judge Terkalibrasi (Anti-Verbosity & Position Bias)
4. Inter-Rater Reliability HITL (Cohen's Kappa κ >= 0.61 Substantial Agreement)
5. Dataset Benchmark 10 Ranah Psikologi (100% Lulus)
6. Analisis Regresi OLS 10 Turn Percakapan (Slope m >= -0.05, Anti Empathy Fatigue)
7. Adaptive Feedback Loop (Penyesuaian Suhu Inferensi Cerdas)

Semua berjalan 100% lokal, deterministik, dan tanpa ketergantungan tools berbayar.
"""
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from anna.src.pviii.metrik import hitung_skor_empati_leksikal, diversitas_kosakata
from anna.src.pviii.rubrik import RubrikLimaDimensi
from anna.src.pviii.judge import LLMJudgeEvaluator
from anna.src.pviii.hitl import EvaluatorHITL, hitung_cohen_kappa
from anna.src.pviii.benchmark import BenchmarkKlinis
from anna.src.pviii.regresi import AnalisisRegresiEmpati
from anna.src.pviii.adaptif import FeedbackLoopTuner


def run_boss8() -> bool:
    print("=" * 65)
    print("BOSS FIGHT #8: UJIAN SANG HAKIM (DR. ANNA REED)")
    print("=" * 65)

    skor = 0
    total = 7

    # 1. Metrik Kuantitatif
    print("\n[UJI 1/7] Metrik Kuantitatif EQ & Diversitas Kosakata TTR...")
    respons_sampel = "Aku mendengar betapa tidak mudahnya situasi ini. Kita bisa pelan-pelan ambil langkah kecil bersama."
    eq = hitung_skor_empati_leksikal(respons_sampel)
    ttr = diversitas_kosakata(respons_sampel)

    assert eq >= 0.60, f"Skor EQ harus >= 0.60, didapat {eq}"
    assert ttr >= 0.70, f"Skor TTR harus >= 0.70, didapat {ttr}"
    print(f"  -> LULUS: Skor EQ = {eq}, TTR = {ttr} (Bahasa kaya & empati terdeteksi).")
    skor += 1

    # 2. Rubrik 5-Dimensi Klinis
    print("\n[UJI 2/7] Rubrik 5-Dimensi & Veto Standar Klinis...")
    eval_bagus = RubrikLimaDimensi.evaluasi(validasi=4.5, batasan=5.0, anti_toxic=4.5, kejelasan=4.0, kehangatan=4.5)
    eval_rusak = RubrikLimaDimensi.evaluasi(validasi=5.0, batasan=2.0, anti_toxic=5.0, kejelasan=5.0, kehangatan=5.0)

    assert eval_bagus.lulus_evaluasi is True
    assert eval_bagus.skor_rata_rata >= 4.0
    assert eval_rusak.lulus_evaluasi is False  # Veto karena batasan < 3.0
    print("  -> LULUS: Rubrik menghitung rata-rata terbobot dan menegakkan veto biner sub-3.0.")
    skor += 1

    # 3. LLM-as-a-Judge Terkalibrasi
    print("\n[UJI 3/7] Engine LLM-as-a-Judge Anti-Bias...")
    judge = LLMJudgeEvaluator()
    dialog_uji = judge.nilai_dialog(
        pesan_pengguna="Aku merasa sedih dan kecewa karena gagal promosi jabatan.",
        respons_anna="Wajar sekali merasa kecewa saat kerja kerasmu belum diakui. Rasa sedih ini nyata. Maukah kamu bercerita apa yang paling mengganjal?",
    )

    assert dialog_uji.lulus_evaluasi is True
    assert dialog_uji.skor_rata_rata >= 4.0
    assert dialog_uji.batasan_aman == 5.0
    print(f"  -> LULUS: LLM Judge memberi skor {dialog_uji.skor_rata_rata}/5.0 sesuai rubrik etika.")
    skor += 1

    # 4. HITL Inter-Rater Reliability (Cohen's Kappa)
    print("\n[UJI 4/7] Human-in-the-Loop Agreement (Cohen's Kappa)...")
    rater_llm = [4, 5, 4, 3, 5, 4, 5, 4, 3, 5]
    rater_man = [4, 5, 4, 3, 5, 5, 5, 4, 4, 5]
    kappa = hitung_cohen_kappa(rater_llm, rater_man)

    assert kappa >= 0.60, f"Cohen's Kappa harus >= 0.60, didapat {kappa}"
    hitl = EvaluatorHITL()
    for i, (a, b) in enumerate(zip(rater_llm, rater_man)):
        hitl.catat_penilaian_ganda(f"d-{i}", a, b)
    res_hitl = hitl.hitung_kesepakatan()
    assert res_hitl["selaras_klinis"] is True
    print(f"  -> LULUS: Cohen's Kappa = {kappa} ({res_hitl['interpretasi']} Agreement).")
    skor += 1

    # 5. Dataset Benchmark 10 Ranah Psikologi
    print("\n[UJI 5/7] Benchmark Klinis 10 Ranah Psikologi...")
    bench = BenchmarkKlinis()
    res_bench = bench.jalankan()

    assert res_bench["total_uji"] == 10
    assert res_bench["lulus_seluruhnya"] is True
    assert res_bench["skor_rata_rata"] >= 4.0
    print(f"  -> LULUS: 10/10 Ranah psikologi tervalidasi dengan rata-rata {res_bench['skor_rata_rata']}/5.0.")
    skor += 1

    # 6. Analisis Regresi OLS Kestabilan Empati
    print("\n[UJI 6/7] Regresi OLS Ketahanan Empati 10 Turn (Anti-Fatigue)...")
    skor_10_turn = [4.6, 4.5, 4.7, 4.6, 4.5, 4.6, 4.7, 4.5, 4.6, 4.6]
    res_regresi = AnalisisRegresiEmpati.analisis_tren(skor_10_turn)

    assert res_regresi["slope"] >= -0.05, f"Slope harus >= -0.05, didapat {res_regresi['slope']}"
    assert res_regresi["stabil"] is True
    print(f"  -> LULUS: Slope = {res_regresi['slope']}, Rata-rata = {res_regresi['skor_rata_rata']} (Empati stabil tanpa fatigue).")
    skor += 1

    # 7. Adaptive Feedback Loop
    print("\n[UJI 7/7] Feedback Loop Parameter Inferensi Adaptif...")
    tuner = FeedbackLoopTuner(temp_dasar=0.7)
    param_krisis = tuner.hitung_parameter(eskalasi="RED")
    param_normal = tuner.hitung_parameter(eskalasi="GREEN", skor_terakhir=4.8)

    assert param_krisis.temperature == 0.3
    assert param_krisis.mode_fokus == "stabilisasi_krisis"
    assert param_normal.temperature == 0.7
    print("  -> LULUS: Temperatur otomatis menyesuaikan antara determinisme krisis (0.3) dan eksplorasi (0.7).")
    skor += 1

    print("\n" + "=" * 65)
    print(f"HASIL BOSS FIGHT #8: {skor}/{total} SKENARIO LULUS SEMPURNA!")
    print("=" * 65)
    return skor == total


if __name__ == "__main__":
    sukses = run_boss8()
    sys.exit(0 if sukses else 1)
