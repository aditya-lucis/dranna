# Dr. Anna Reed — AI Companion (Project Serenity)

> *"An AI Companion that listens with empathy, knows its limits, and encourages real healing."*  
> — **Aditya Lucis Caelum (2026 Edition)**

![Dr. Anna Reed](assets/img/01134ab7-5052-4e91-9d6a-7753694fe140.webp)

**Dr. Anna Reed** adalah sistem pendamping kesehatan mental cerdas (*Mental Health AI Companion*) yang dibangun secara berstruktur, etis, dan berbasis bukti sains. Proyek ini memadukan kehangatan persona (sebagai AI Waifu / AI Companion / AI Sister) dengan logika keselamatan berlapis (*hard-gate*) dan fondasi matematika transparan menggunakan **Python 3.12**, **NumPy 2.5**, **LangChain 1.x**, **LangGraph 1.2**, **FastAPI 0.141**, dan **PostgreSQL 18**.

---

## 🐾 Karakter & Persona

* **Dr. Anna Reed**: Pendamping kesehatan mental berpengetahuan terstruktur, lembut, *soft-spoken*, dan pendengar yang berhati-hati.
* **Kucing Pendamping**:
  * **Reno**: Kucing tuxedo hitam-putih yang suka tidur di bahu Anna.
  * **Rude**: Kucing tabby pemalu yang meringkuk di sofa.
* **Tiga Gaya Interaksi (Style Governor)**:
  * **Netral (Default)**: Tenang, profesional, reflektif.
  * **AI Waifu**: Feminin lembut, *playful* ringan, dipilih sadar oleh pengguna dewasa.
  * **AI Sister**: Relasi persaudaraan hangat, tidak menggurui.
  * **Hard-Gate Keselamatan**: Saat terdeteksi risiko eskalasi $\ge \text{ORANGE}$, seluruh persona nonaktif seketika menjadi bahasa netral-tenang dan jalur darurat aktif.

---

## 🛡️ Tiga Gerbang Kualitas (Harness Ritual)

Sebelum setiap commit dilakukan, tiga gerbang pemeriksaan wajib berstatus hijau:

```bash
python tools/harness_check.py
```

1. **`doctor`**: Verifikasi integritas dependensi dan lingkungan stabil 2026.
2. **`uzur`**: Scanner anti-API usang (`tools/ban_deprecated.py`).
3. **`tests`**: Pengujian unit komprehensif (kategori normal, ambigu, dan krisis-sintetis).

---

## 📚 Dokumen Fondasi (Phase 0)

* [Surat Niat Batas Sistem](docs/serenity-intent.md): Kapan Anna wajib berhenti bicara dan merujuk ke manusia nyata.
* [Kontrak Etika WHO & Tavory](docs/ethics-contract.md): Pemetaan prinsip etika internasional ke dalam invarian mesin.
* [Peta Empat Pilar Matematika](docs/math-map.md): Keterkaitan statistika, kalkulus, diskrit, dan aljabar linear ke berkas kode.
* [Tracing Latensi Satu Pesan, Dua Nasib](docs/trace-insomnia.md): Alur happy path vs jalur krisis $< 200\text{ ms}$.
