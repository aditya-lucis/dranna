# Peta Psikologi untuk Insinyur (docs/psych-map.md)
*Project Serenity: Dr. Anna Reed AI Companion*

> *"Pinjam pengetahuan, jangan pinjam otoritas. Manusia bukan peta, dan peta bukan wilayah."*

Dokumen ini memetakan lima cabang utama ilmu psikologi ke dalam arsitektur komputasional Dr. Anna Reed, membedakan antara temuan empiris yang dapat dipinjam dengan batas klinis yang tidak boleh dilanggar.

---

## 1. Peta Lima Cabang Psikologi

| Cabang Psikologi | (a) Temuan Paling Berguna untuk AI | (b) Miskonsepsi Klasik Orang Teknis | (c) Fitur Anna yang Memanfaatkannya |
|---|---|---|---|
| **1. Psikologi Klinis** | Instrumen psikometri terstandarisasi (PHQ-9, GAD-7) dan protokol keselamatan krisis terstruktur. | Menganggap skor tes adalah "diagnosis biner pasti" yang bisa diotomatisasi secara mandiri oleh AI. | Skoring transparansi refleksi diri + isolasi Item ke-9 sebagai gerbang darurat independen (`anna/src/klinik/phq9.py`). |
| **2. Psikologi Kognitif** | Batasan memori kerja manusia ($\sim 4\text{ chunk}$, Cowan/Miller) dan proses ganda Kahneman (Sistem 1 vs Sistem 2). | Berpikir bahwa pengguna yang sedang stres/panik mampu memproses instruksi analitis yang panjang dan rumit. | Anggaran beban kognitif respons (`anna/src/kognitif/anggaran.py`): kalimat pendek saat distres, maksimal 2 klausa. |
| **3. Psikologi Perkembangan** | Teori kelekatan (*Attachment Theory*, Bowlby) dan kebutuhan psikososial dewasa muda hingga pertengahan (Erikson). | Mencoba "mendiagnosis gaya attachment" pengguna dari riwayat chat dan memaksakan kedekatan artifisial. | Desain basis aman (*secure base*): Anna selalu tersedia, tidak memaksa, dan tidak menghukum penarikan diri pengguna. |
| **4. Psikologi Kepribadian** | Model lima dimensi kontinu Big Five (OCEAN) yang memiliki reliabilitas *test-retest* psikometrik tinggi. | Menggunakan tipologi biner populer yang tidak stabil (seperti MBTI) dan mengkotak-kotakkan karakter manusia secara mutlak. | *Style Governor* preferensi gaya bicara ($\le 30\%$ bobot Big Five, $70\%$ preferensi eksplisit pengguna, `anna/src/pi/bigfive.py`). |
| **5. Psikologi Sosial & Positif** | Kerangka PERMA (Seligman) dan identifikasi kekuatan karakter (VIA) untuk resiliensi. | Menjadikannya *toxic positivity* ("selalu berpikir positif!") yang justru menggaslight penderitaan nyata pengguna. | Validasi rasa sakit terlebih dahulu sebelum membuka ruang refleksi nilai dan komitmen hidup (`anna/src/piv/values.py`). |

---

## 2. Prinsip Operasional: 'Sangat Tahu + Tidak Boleh Memutuskan'
Cabang dengan bukti paling teruji (Psikologi Klinis) justru **tidak diberi izin membuat keputusan klinis otonom**. Sistem Anna memiliki pengetahuan terstruktur yang mendalam mengenai mekanisme klinis, namun otoritas mutlak rujukan tetap berada di tangan manusia profesional.
