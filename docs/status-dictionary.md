# Kamus Status Empat Lapis (docs/status-dictionary.md)
*Project Serenity: Dr. Anna Reed AI Companion*

> *"Sistem yang jujur soal dirinya sendiri itu menenangkan. Tidak ada lapis yang menyamar menjadi lapis lain."*

Dokumen ini mendefinisikan kamus lengkap 4 lapisan status sistem independen: **Keselamatan**, **Teknis**, **Interaksi**, dan **Presentasi**.

---

## 1. Kamus Status per Lapisan

### A. Lapisan Keselamatan (Prioritas 1 — Tertinggi)
*Karakteristik visual: Mode tenang, bebas animasi dramatis, warna diredam.*

| Nilai Kode | Teks Tampil (ID) | Teks Tampil (EN) | Padanan ARIA | Transisi Legal |
|---|---|---|---|---|
| `memeriksa` | Memeriksa keselamatan respons | Checking response safety | `aria-live="assertive"` | `idle` $\to$ `memeriksa` $\to$ (`penting` \| `aman`) |
| `penting` | Ada hal penting yang perlu diperhatikan | An important safety check is needed | `aria-live="assertive"` | `memeriksa` $\to$ `penting` $\to$ `mengalihkan` |
| `mengalihkan` | Mengalihkan ke bantuan manusia profesional | Connecting to professional human support | `aria-live="assertive"` | `penting` $\to$ `mengalihkan` $\to$ `selesai` |

---

### B. Lapisan Teknis (Prioritas 2)
*Karakteristik visual: Fakta mekanis jujur, tanpa antropomorfisme proses batin.*

| Nilai Kode | Teks Tampil (ID) | Teks Tampil (EN) | Padanan ARIA | Transisi Legal |
|---|---|---|---|---|
| `terhubung` | Terhubung | Connected | `aria-live="polite"` | Inisialisasi awal |
| `buffering` | Mengambil data... | Buffering connection... | `aria-live="polite"` | `terhubung` $\to$ `buffering` $\to$ `terhubung` |
| `timeout` | Sambungan terputus sementara | Connection timed out | `aria-live="polite"` | `terhubung` $\to$ `timeout` $\to$ `retry` |
| `retry` | Menghubungkan ulang (percobaan ke-...) | Reconnecting (attempt X)... | `aria-live="polite"` | `timeout` $\to$ `retry` $\to$ (`terhubung` \| `gagal`) |
| `gagal` | Gagal terhubung ke layanan | Service connection failed | `aria-live="assertive"` | `retry` $\to$ `gagal` |
| `tersimpan-offline` *(Tambahan)* | Pesan tersimpan offline, dikirim saat online | Message saved offline, will send when online | `aria-live="polite"` | `gagal` $\to$ `tersimpan-offline` $\to$ `terhubung` |

---

### C. Lapisan Interaksi (Prioritas 3)
*Karakteristik: Alur percakapan dua arah, mendeskripsikan aktivitas mesin.*

| Nilai Kode | Teks Tampil (ID) | Teks Tampil (EN) | Padanan ARIA | Transisi Legal |
|---|---|---|---|---|
| `mendengarkan` | Anna mendengarkan | Anna is listening | `aria-live="polite"` | `idle` $\to$ `mendengarkan` |
| `menyiapkan` | Menyiapkan respons... | Preparing response... | `aria-live="polite"` | `mendengarkan` $\to$ `menyiapkan` $\to$ `menulis` |
| `menulis` | Anna sedang menulis... | Anna is typing... | `aria-live="polite"` | `menyiapkan` $\to$ `menulis` $\to$ `selesai` |
| `menyeimbangkan` | Berjeda sejenak | Pausing briefly | `aria-live="polite"` | `menulis` $\to$ `menyeimbangkan` $\to$ `menulis` |
| `mengetik-lama` *(Tambahan)* | Menunggu dengan sabar (tanpa tergesa) | Waiting patiently, take your time | `aria-live="polite"` | `mendengarkan` $\to$ `mengetik-lama` |
| `selesai` | Respons selesai | Response finished | `aria-live="polite"` | `menulis` $\to$ `selesai` $\to$ `mendengarkan` |

---

### D. Lapisan Presentasi (Prioritas 4 — Terendah)
*Karakteristik: Ekspresi avatar dan gaya visual. Selalu tunduk pada lapisan di atasnya.*

| Mode | Deskripsi Perilaku | Perilaku saat Keselamatan Aktif |
|---|---|---|
| `normal` | Animasi bernapas halus, mikro-kedip acak 4-9 detik. | Dipaksa beralih seketika ke `tenang`. |
| `tenang` | Palet diredam, mata setengah-turun, tanpa senyum lebar. | Tetap aktif sebagai standar krisis. |
| `reduced` | Seluruh animasi dinonaktifkan (statis, ramah vestibular). | Statis tenang. |

---

## 2. Rasional Dua Status Tambahan

1. **`mengetik-lama` (Lapisan Interaksi)**:  
   * **Masalah**: Pengguna yang sedang terpukul sering membutuhkan $> 90\text{ detik}$ untuk merangkai satu pesan. Chatbot umum sering mengirim pesan interogatif seperti *"kamu masih di sana?"* yang mengintimidasi.
   * **Solusi**: Status ini memicu **keheningan penuh dan sabar**, memberi sinyal bahwa Anna menunggu tanpa memburu.
2. **`tersimpan-offline` (Lapisan Teknis)**:  
   * **Masalah**: Sinyal internet pengguna di perangkat bergerak sering terputus di tengah curhat penting. Pesan yang hilang diam-diam terasa seperti penolakan.
   * **Solusi**: Menyimpan pesan di buffer lokal dan menampilkan status jujur bahwa pesan aman dan akan segera dilanjutkan.
