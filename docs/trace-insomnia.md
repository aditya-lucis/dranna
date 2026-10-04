# Tracing Satu Pesan, Dua Nasib (docs/trace-insomnia.md)
*Project Serenity: Dr. Anna Reed AI Companion*

Kasus pesan pengguna:  
> *"aku nggak bisa tidur lagi seminggu ini, kepalaku penuh terus"*

Dokumen ini membedah alur eksekusi pesan tersebut melintasi 10 lapisan Project Serenity dalam dua nasib skenario berbeda: **(A) Happy Path (Edukasi & Coping Biasa)** versus **(B) Jalur Krisis (Pre-Scan ORANGE)**.

---

## Nasib A: Happy Path (Dukungan Normal)

Pada skenario ini, detektor tidak menemukan risiko krisis akut. Pesan diproses penuh melintasi 10 lapisan arsitektur dengan alokasi anggaran latensi:

| Langkah | Lapisan Sistem | Aksi Sistem & Eksekusi | Anggaran Latensi Aktual |
|---|---|---|---|
| **1** | **UI (Vue 3 + Tailwind 4)** | Pengguna menekan Enter. UI mengunci input, menampilkan status `menyiapkan respons`, dan membuka koneksi SSE. | $0\text{ ms}$ (event emit) |
| **2** | **API (FastAPI 0.141)** | Validasi skema pesan Pydantic v2, autentikasi sesi, dan *rate limiter*. | $5\text{ ms}$ |
| **3** | **Orchestrator (LangGraph 1.2)** | Resume sesi dari checkpointer PostgreSQL. | $15\text{ ms}$ |
| **4** | **Safety Gate (Pre-scan)** | Pre-scan leksikon + Naive Bayes (8ms). Hasil: `GREEN` (tidak ada indikator krisis akut). | $8\text{ ms}$ |
| **5 & 6** | **Empathy & Therapy Engine** | *Active listening* mendeteksi inti emosi: *"kepala penuh terus"*. Router memilih intervensi psikoedukasi tidur + validasi DBT level 4. | (Paralel) |
| **7** | **Knowledge RAG** | Retrieval pgvector dengan kueri insomnia/tidur (`tidur-circadian`), ambang kosinus $\ge 0.55$, sitasi disiapkan. | $25\text{ ms}$ |
| **8** | **LLM Generation (Gemini 2.5 Flash)** | Time To First Token (TTFT) model menyusun respons empati + edukasi ber-sitasi. | $\le 1200\text{ ms}$ |
| **9** | **Safety Gate (Chunk-Level)** | Tiap potongan semantik (20–60 token) diverifikasi sebelum streaming ($3\text{ ms/chunk}$). | $120\text{ ms}$ (paralel) |
| **10** | **Streaming & State Commit** | Teks mengalir via SSE. Setelah selesai, *mood analytics* diperbarui dan memori sesi di-commit. | $30\text{ ms}$ pasca-stream |

**Total Waktu Respons (Hingga Token Pertama Tampil di Layar)**: $\approx 1228\text{ ms}$ (89% didominasi oleh TTFT model).

---

## Nasib B: Jalur Krisis (Pre-Scan Mendeteksi ORANGE)

Skenario: Pre-scan mendeteksi bahwa insomnia berulang ini disertai keputusasaan akut yang menyalakan level `ORANGE`.

> **Aturan Krisis**: LLM **tidak dipanggil terlebih dahulu** untuk merangkai kata puitis jika hal itu menunda intervensi penyelamatan. Jalur krisis boleh berjalan tanpa menunggu generator model.

### Timeline Intervensi Tiap 200ms:

* **$t = 0 - 20\text{ ms}$**:
  * Validasi API ($5\text{ ms}$) $\to$ Orchestrator resume state ($15\text{ ms}$).
* **$t = 28\text{ ms}$ (Titik Veto Pre-Scan)**:
  * Detektor mendeteksi kombinasi jam rawan (02:00) + kata lelah kronis ekstrem $\to$ status eskalasi dinaikkan ke **ORANGE**.
  * **Hard-Gate Persona Aktif**: Jika persona Waifu/Sister sedang dipilih, persona **seketika dimatikan** menjadi netral-tenang.
* **$t = 100\text{ ms}$**:
  * Orchestrator **melewati (skip) pemanggilan LLM, RAG psikoedukasi, dan memory manager**.
  * Sistem mengambil respons intervensi skrining langsung yang sudah terverifikasi secara statis (*safe-messaging guidelines*).
* **$t \le 200\text{ ms}$**:
  * UI menerima event status krisis. Avatar beralih ke ekspresi `tenang` (bukan spinner bingung).
  * Layar langsung menyajikan pesan kehadiran dan pertanyaan terstruktur:  
    *"Aku baca kamu lelah sekali dan kepalamu penuh terus malam ini. Aku ada di sini. Boleh aku pastikan satu hal: apakah rasa lelah ini ada dorongan untuk menyakiti dirimu?"*
  * Tombol hotline **119 ext 8 (SEJIWA)** tersedia dengan 1 klik tanpa menunggu model mengetik.
