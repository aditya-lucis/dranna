# Peta Matematika Empat Pilar (Math Map)
*Project Serenity: Dr. Anna Reed AI Companion*

> *"Empat pilar, satu bahasa. Angka yang bisa dijelaskan adalah bentuk paling tua dari rasa hormat."*

Dokumen ini memetakan empat fondasi matematika komputasional ke dalam modul kode nyata yang diimplementasikan di seluruh sistem Dr. Anna Reed.

---

## 1. Matriks 4 Pilar × Tugas Nyata Kode

| Pilar Matematika | Tugas Arsitektural / Fungsional | Berkas Implementasi Kode | Peran & Formulasi Kunci |
|---|---|---|---|
| **1. Statistika** | **Evaluasi Detektor & Sensitivitas** | `anna/src/pi/08_detektor.py` & `tests/test_detektor.py` | Kurva ROC, kalibrasi *miss-rate* $\le 5\%$, seleksi *cut-off* dengan kompensasi FP yang terukur. |
| | **Skoring Psikometri Klinis** | `anna/src/klinik/phq9.py` & `anna/src/piii/02_anxietas.py` | Skoring PHQ-9 (0–27) dan GAD-7 (0–21) dengan pemisahan *hard-gate* Item ke-9. |
| | **Estimasi Ketidakpastian & Kalibrasi** | `anna/src/pi/04_bootstrap.py` & `04_kalibrasi.py` | Interval kepercayaan Student-t, bootstrap nonparametrik, dan Expected Calibration Error (ECE $\le 0.10$). |
| | **Penalaran Bayesian & Log-Odds** | `anna/src/pi/05_bayes.py` & `05_prior.py` | $\text{odds}_{\text{posterior}} = \text{odds}_{\text{prior}} \times \text{LR}$, klaster dependensi bukti, mitigasi *Base Rate Neglect*. |
| **2. Kalkulus** | **Optimisasi Detektor Distres dari Nol** | `anna/src/pi/07_gradien.py` | Gradient descent manual: $w \leftarrow w - \eta \nabla L$, *learning rate* adaptif, stabilitas floating point. |
| | **Loss Function Asimetris Berbobot** | `anna/src/pi/07_gradien.py` | Binary Cross-Entropy berbobot ($\alpha = 0.7$) untuk menghukum kesalahan *False Negative* distres lebih berat. |
| | **Laju Dinamika Suasana (*Mood Velocity*)** | `anna/src/pi/01_circumplex.py` & `anna/src/mood/timeline.py` | Turunan numerik $v(t) = \frac{\Delta e(t)}{\Delta t}$ untuk mendeteksi perubahan emosi tajam antar-sesi. |
| | **Pacing Pernapasan Sinusoidal** | `anna/src/piv/11_breathing.py` | Gelombang sinusoidal periode 10 detik ($0.1\text{ Hz}$) untuk resonansi *heart rate variability* (HRV). |
| **3. Matematika Diskrit** | **Logika Aturan Keselamatan (Proposisi)** | `anna/src/pi/10_logika.py` & `anna/src/reset/contract.py` | Penegakan de Morgan $\neg(A \wedge B) \equiv \neg A \vee \neg B$, short-circuit murah-ke-mahal, evaluasi *truth-table*. |
| | **State Machine Percakapan & Histeresis** | `anna/src/pi/11_fsm.py` & `anna/src/agent/state_machine.py` | Matriks transisi adjacency boolean $T[i,j]$, uji *reachability* BFS, histeresis asimetris (naik 1 sinyal, turun butuh 2 sinyal + waktu). |
| | **Analisis Jaringan Dukungan Sosial (Graf)** | `anna/src/pi/12_graf.py` & `anna/src/crisis/safety_plan.py` | Representasi graf berbobot simpul sosial, pencarian jarak BFS, verifikasi redundansi jalur bantuan darurat. |
| | **Model Persetujuan Berbasis Himpunan** | `anna/src/etika/consent.py` | Operasi interseksi konjungtif 5 komponen izin pengguna sebelum pengaktifan sensor/fitur. |
| **4. Aljabar Linear** | **Ruang Emosi Circumplex 2D** | `anna/src/pi/01_circumplex.py` | Koordinat afektif $(Valence, Arousal) \in [-1, 1]^2$, jarak Euclidean, dan partisi kuadran. |
| | **Embedding Semantik & Jarak Kosinus** | `anna/src/pi/13_vektor.py` & `anna/src/piii/01_retrieval.py` | Vektor 768 dimensi, normalisasi L2 ($\|v\|_2 = 1$), perkalian dot-product cepat untuk pencarian psikoedukasi. |
| | **Mini Scaled Dot-Product Attention** | `anna/src/pi/14_attention.py` | $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V$, matriks kohesi sesi, dan entropi fokus. |
| | **Proyeksi Longitudinal SVD / PCA** | `anna/src/pi/15_pca.py` & `anna/src/mood/pca_analytics.py` | Dekomposisi nilai singular $X_c = U \Sigma V^T$, rasio variansi $\ge 80\%$, deteksi anomali residu MAD. |

---

## 2. Tingkat Penguasaan & Rencana Verifikasi

* **Pilar yang Sangat Dikuasai (Siap Produksi)**:
  * Aljabar linear representasi vektor & matriks attention.
  * Logika diskrit state machine dan hukum de Morgan.
  * Formulasi kalkulus fungsi loss berbobot & gradient clipping.
* **Pilar yang Memerlukan Kalibrasi Ekstra Ketat**:
  * Statistika Bayesian pada prevalensi rendah (*Base Rate Neglect*): Membutuhkan uji empiris terus-menerus agar tidak terjadi tuduhan berlebih terhadap pengguna normal.
  * Residu PCA untuk deteksi hari anomali: Harus dipastikan berakar pada deviasi absolut median (MAD) agar hari ekstrem tidak menggeser batas ambangnya sendiri.
