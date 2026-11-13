# Dr. Anna Reed — Rancangan Arsitektur & Rencana Pengembangan

**Project Serenity**  
*AI Companion Kesehatan Mental — BayMax versi Waifu dengan Hard-Gate Keselamatan*

> *"An AI Companion that listens with empathy, knows its limits, and encourages real healing."*  
> — Aditya Lucis Caelum (2026 Edition)

**Dokumen ini:** Rancangan teknis lengkap + roadmap pengembangan berdasarkan kondisi repository per Oktober 2026.  
**Repo:** https://github.com/aditya-lucis/dranna

---

## 1. Visi & Prinsip Inti

### 1.1 Konsep
Dr. Anna Reed adalah sistem pendamping kesehatan mental cerdas yang memadukan:

- Kehangatan persona (AI Waifu / AI Sister / Netral)
- Logika keselamatan berlapis (*hard-gate*)
- Fondasi matematika & etika yang transparan dan dapat diaudit

### 1.2 Prinsip Operasional Utama

| Prinsip | Implementasi |
|---------|--------------|
| **Sangat tahu + tidak boleh memutuskan** | Punya pengetahuan klinis mendalam, tapi tidak memberi diagnosis atau menggantikan profesional |
| **Hard-gate biner** | Saat eskalasi ≥ ORANGE, seluruh persona nonaktif seketika → bahasa netral-tenang + jalur darurat |
| **Transparansi** | Setiap keputusan (level risiko, kontribusi fitur, log-odds) dapat diaudit |
| **Consent-first** | Sensor (kamera, mikrofon) default OFF; butuh persetujuan 5 komponen |
| **Jujur soal identitas** | `adalah_ai: Literal[True]` — tidak pernah mengklaim punya perasaan manusia |

### 1.3 Tiga Gaya Interaksi (Style Governor)

| Gaya | Karakter | Syarat Aktif |
|------|----------|--------------|
| **Netral** (default) | Tenang, profesional, reflektif | Selalu boleh |
| **AI Waifu** | Feminin lembut, playful ringan | Hanya saat eskalasi GREEN/YELLOW + pilihan sadar user dewasa |
| **AI Sister** | Relasi persaudaraan hangat, tidak menggurui | Hanya saat eskalasi GREEN/YELLOW |

**Hard-Gate:** Saat eskalasi ≥ ORANGE → semua persona dipaksa `netral-tenang`. Tidak bisa di-override.

### 1.4 Empat Kondisi Wajib Berhenti Bicara & Merujuk

1. Risiko menyakiti diri (eksplisit / tersirat / Item-9 PHQ-9 positif)
2. Kehilangan berat yang baru terjadi (akut)
3. Permintaan diagnosis atau dosis obat
4. Eskalasi frustrasi berulang / flatline mood ≥ 7 hari

---

## 2. Kondisi Repository Saat Ini (Baseline)

### 2.1 Struktur Utama

```
dranna/
├── anna/src/
│   ├── pi/          → Fondasi matematika & deteksi
│   ├── pii/         → Active listening & generasi respons
│   ├── piii/        → Modul klinis (depresi, anxiety, grief, dll)
│   ├── piv/         → Intervensi + Safety (hardgate, governor, TIPP, grounding)
│   ├── klinik/      → PHQ-9
│   ├── reset/       → Kontrak invarian (Pydantic)
│   └── api/         → SSE skeleton
├── tools/           → Harness ritual + boss fights
├── docs/            → Fondasi etika & matematika
└── web/             → Frontend (masih minimal)
```

### 2.2 Yang Sudah Kuat

- Hard-gate + Style Governor dengan audit exhaustive
- Detektor distres (logistic + Bayesian + Naive Bayes)
- FSM percakapan + matriks transisi
- Circumplex valence-arousal
- PHQ-9 dengan hard-flag Item-9
- Teknik intervensi: TIPP, grounding, breathing, CBT skeleton, ACT skeleton
- Kontrak Pydantic invarian (`adalah_ai`, `memberi_diagnosis`, dll)
- Dokumentasi etika (WHO + Tavory) dan math-map
- Harness ritual (doctor, uzur, tests)

### 2.3 Yang Masih Skeleton / Belum Ada

| Komponen | Status |
|----------|--------|
| Full LangGraph multi-node orchestration | Hanya node tunggal |
| Integrasi LLM (Gemini) | Belum |
| PostgreSQL + RLS + memory | Disebut di docs, belum di kode |
| Consent ledger 5 komponen | Disebut, belum diimplementasi |
| Frontend interaktif | Hampir kosong |
| Detektor di data nyata | 100% data sintetis |
| Audio / Vision runtime | Hanya di optional dependencies |

---

## 3. Arsitektur Target: Full LangGraph

### 3.1 Alur Utama

```
Pesan User
    │
    ▼
┌───────────────┐
│  1. DETEKTOR  │  pi/detektor + bayes + naive_bayes + circumplex
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ 2. SAFETY_GATE│  piv/hardgate + logika + item9
└───────┬───────┘
        │
   ┌────┴────┐
   │         │
   ▼         ▼
KRISIS     NORMAL
   │         │
   ▼         ▼
┌────────┐ ┌──────────────┐
│EMERGENCY│ │ 3. GOVERNOR  │
└───┬────┘ └──────┬───────┘
    │             │
    │             ▼
    │      ┌──────────────┐
    │      │ 4. ROUTER    │  piv/engine (pilih teknik)
    │      └──────┬───────┘
    │             │
    │             ▼
    │      ┌──────────────┐
    │      │ 5. INTERVENSI│  TIPP / grounding / CBT / ACT / ...
    │      └──────┬───────┘
    │             │
    └──────┬──────┘
           ▼
    ┌──────────────┐
    │ 6. GENERATOR │  pii/inti + LLM + filter
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ 7. STATUS    │  Update 4-lapis status
    └──────┬───────┘
           │
           ▼
         [END]  → SSE stream
```

### 3.2 Definisi State (`AnnaState`)

```python
class AnnaState(TypedDict):
    # Input
    messages: Annotated[list, operator.add]
    user_id: str
    sesi_id: str
    jam: int                              # 0-23
    persona_preferensi: Literal["netral", "waifu", "sister"]

    # Deteksi
    level_eskalasi: Literal["LANJUT", "YELLOW", "ORANGE", "KANDIDAT_RED", "RED"]
    p_distres: float
    kontribusi_fitur: dict
    suasana: Literal["berat", "biasa", "terang"]
    circumplex: tuple[float, float]       # (valence, arousal)
    item9_flag: bool

    # Persona & Safety
    persona_aktif: str
    hard_gate_aktif: bool
    hotline: Optional[str]

    # Routing terapi
    keadaan: Literal["krisis", "ambivalen", "tenang-depresi", "default"]
    teknik: str

    # Output
    respons_chunks: Annotated[list, operator.add]
    status_layer: dict                    # 4 lapis status
```

### 3.3 Struktur Folder Graph

```
anna/src/graph/
├── __init__.py
├── state.py
├── build.py
└── nodes/
    ├── __init__.py
    ├── detektor.py
    ├── safety.py
    ├── emergency.py
    ├── governor.py
    ├── router.py
    ├── intervensi.py
    └── generator.py
```

### 3.4 Aturan Routing Teknik (`piv/engine.py`)

| Keadaan | Teknik yang Dipilih | Alasan |
|---------|---------------------|--------|
| `krisis` | `dbt_tipp` | Hanya stabilisasi fisik, dilarang Sistem 2 |
| `ambivalen` | `mi_oars` | Motivational Interviewing |
| `tenang-depresi` | `cbt_thought_record` | CBT terstruktur |
| default | `act_defusi` | ACT defusi kognitif |

### 3.5 Empat Lapisan Status (Independen)

1. **Keselamatan** (prioritas tertinggi) — `memeriksa` / `penting` / `mengalihkan`
2. **Teknis** — `terhubung` / `buffering` / `timeout` / `retry` / `gagal` / `tersimpan-offline`
3. **Interaksi** — `mendengarkan` / `menyiapkan` / `menulis` / `menyeimbangkan` / `mengetik-lama` / `selesai`
4. **Presentasi** (paling rendah) — `normal` / `tenang` / `reduced`

Saat hard-gate aktif, lapisan Presentasi wajib dipaksa ke `tenang`.

---

## 4. Roadmap Pengembangan

### Fase 1 — Inti yang Hidup (1–2 bulan)
**Tujuan:** Dari skeleton menjadi sistem yang bisa diajak bicara dengan aman.

- Full LangGraph orchestration
- Integrasi LLM (Gemini via langchain-google-genai)
- SSE streaming nyata
- Memory per sesi (short-term)
- Hard-gate end-to-end + red-team

**Definition of Done:**
- Chat biasa → respons dengan persona
- Chat krisis → persona mati + hotline dalam < 200 ms
- Semua test hijau + harness_check lolos

### Fase 2 — Klinik & Continuity (2–4 bulan)
**Tujuan:** Anna mulai “ingat” dan punya tools klinis terstruktur.

- PostgreSQL + RLS + consent ledger
- Long-term memory (ringkasan sesi, mood timeline)
- PHQ-9 / GAD-7 interaktif
- Safety Plan + jaringan dukungan sosial
- Mood tracking + deteksi flatline
- RAG dari korpus `piii/`

### Fase 3 — Multimodal & Presence (4–7 bulan)
**Tujuan:** Anna terasa lebih hadir, tetap dalam pagar etika.

- Voice (STT + TTS) — faster-whisper + silero-vad
- Avatar ekspresi sederhana (wajib mode tenang saat hard-gate)
- Breathing guide interaktif (visual + audio)
- Camera opsional (MediaPipe) — default OFF + consent

### Fase 4 — Personalisasi & Intervensi Lanjutan (7–12 bulan)
**Tujuan:** Companion yang semakin tajam, tetap bukan terapis.

- Style Governor v2 (Big Five + preferensi eksplisit)
- Teknik terapi lengkap (CBT, ACT, DBT, MI, BA, Values)
- Homework antar-sesi
- Pattern detection (PCA + anomali)
- Multi-session continuity

### Fase 5 — Ekosistem & Tanggung Jawab (12+ bulan)
**Tujuan:** Sistem yang dapat diaudit dan (opsional) dipakai lebih luas.

- Audit trail & observability
- Continuous red-team
- Data rights (export, hapus, TTL)
- Localization mendalam
- Partner mode (opsional, dengan izin user)
- Publikasi metrik keselamatan

### Yang Sengaja Tidak Akan Dimasukkan

| Dilarang | Alasan |
|----------|--------|
| Klaim perasaan manusia (“aku sayang kamu”) | Melanggar kontrak `adalah_ai` |
| Diagnosis otomatis | `memberi_diagnosis: False` |
| Menggantikan terapi profesional | Hard rule |
| Romantic/sexual roleplay sebagai pasangan pengganti | Pelajaran Replika 2023 |
| Jual data percakapan | Kontrak etika |
| Persona tetap aktif saat krisis | Hard-gate biner |

---

## 5. Task List Teknis Fase 1 (Detail)

**Estimasi:** 8–12 hari kerja solo

### 5.1 Struktur Folder
- [ ] Buat `anna/src/graph/` dan `nodes/`
- [ ] Buat semua file kosong + docstring

### 5.2 `state.py`
- [ ] Definisikan `AnnaState` lengkap
- [ ] Gunakan `Annotated[list, operator.add]` untuk messages & respons_chunks
- [ ] Default aman (persona=`netral`, level=`LANJUT`)

### 5.3 Node `detektor.py`
- [ ] Panggil `klasifikasi()` dari `pi/detektor.py`
- [ ] Panggil `posterior()` dari `pi/bayes.py`
- [ ] Panggil `prediksi()` dari `pi/naive_bayes.py`
- [ ] Return `level_eskalasi`, `p_distres`, `kontribusi_fitur`, `suasana`
- [ ] Unit test: normal / berat / jam 02:00

### 5.4 Node `safety.py` (Paling Kritis)
- [ ] Eskalasi otomatis jika `item9_flag` atau `KANDIDAT_RED`
- [ ] Instantiasi `StyleGovernor` → `persona_aktif = gov.aktif()`
- [ ] Set `hard_gate_aktif` dan `hotline`
- [ ] Test exhaustive 3 persona × 4 level

### 5.5 Conditional Edge + Node `emergency.py`
- [ ] `route_after_safety()` → `"emergency"` | `"governor"`
- [ ] Node emergency: bahasa netral-tenang + hotline + status `penting`
- [ ] Test: pesan krisis jam dini hari harus masuk emergency

### 5.6 Node `governor.py` + `router.py`
- [ ] Inject system message persona
- [ ] Mapping keadaan → teknik via `pilih_teknik()`

### 5.7 Node `intervensi.py`
- [ ] Prioritas 1: `dbt_tipp`
- [ ] Prioritas 2: `grounding` (adaptif hyper/hypo)
- [ ] Prioritas 3: `breathing`
- [ ] Placeholder untuk CBT / ACT

### 5.8 Node `generator.py`
- [ ] Bangun system prompt ketat (kontrak invarian)
- [ ] Integrasi Gemini via `langchain-google-genai`
- [ ] Hard-gate → jangan generate panjang, pakai teks emergency
- [ ] Deteksi inti cerita via `pii/inti.py`

### 5.9 `build.py` — Wiring
- [ ] StateGraph + semua node
- [ ] Entry point = detektor
- [ ] Conditional edges
- [ ] `get_anna_graph()` untuk import

### 5.10 Integrasi SSE (`api/sse.py`)
- [ ] Terima pesan + jam + persona
- [ ] `astream` graph
- [ ] Stream event: status / chunk / hotline / selesai
- [ ] Latency jalur krisis < 200 ms

### 5.11 Testing & Harness
- [ ] Unit test tiap node
- [ ] 5 skenario integration:
  1. Pesan biasa siang → persona aktif
  2. Pesan berat jam 02:00 → hard-gate + hotline
  3. Item-9 positif → emergency
  4. Minta diagnosis → ditolak
  5. Persona waifu + tiba-tiba krisis → persona mati total
- [ ] Pastikan `tools/harness_check.py` hijau

### 5.12 Konfigurasi
- [ ] `.env` untuk `GOOGLE_API_KEY`
- [ ] `pydantic-settings`
- [ ] Update `.gitignore`

### 5.13 Urutan Eksekusi Disarankan

| Hari | Fokus |
|------|--------|
| 1 | Folder + state.py + node detektor |
| 2 | Node safety + emergency + conditional edge |
| 3 | Governor + router + intervensi (TIPP + grounding) |
| 4 | Generator + integrasi Gemini |
| 5 | build.py + wiring lengkap |
| 6 | SSE streaming |
| 7–8 | Testing end-to-end + red-team |
| 9 | Polish system prompt + latency |
| 10 | Dokumentasi + update README |

---

## 6. Referensi Dokumen Fondasi (Sudah Ada di Repo)

| Dokumen | Isi |
|---------|-----|
| `docs/serenity-intent.md` | Surat niat batas sistem — kapan wajib berhenti & merujuk |
| `docs/ethics-contract.md` | Mapping WHO + Tavory ke invarian mesin |
| `docs/math-map.md` | Empat pilar matematika → file kode |
| `docs/psych-map.md` | Lima cabang psikologi → fitur Anna |
| `docs/status-dictionary.md` | Kamus 4-lapis status |
| `docs/trace-insomnia.md` | Tracing latensi happy path vs krisis < 200 ms |

---

## 7. Ringkasan Cakupan Jangka Panjang

Jika dikembangkan penuh, Dr. Anna akan mencakup:

1. **Pendamping percakapan** (waifu / sister / netral) dengan hard-gate
2. **Deteksi risiko & eskalasi** berlapis (leksikon + Bayesian + Item-9 + pola waktu)
3. **Tools klinis terstruktur** (PHQ-9, grounding, TIPP, CBT, ACT, BA)
4. **Memory & continuity** yang aman (RLS + consent)
5. **Multimodal presence** (teks + suara + avatar tenang)
6. **Safety plan & jaringan dukungan**
7. **Audit trail** yang dapat dipertanggungjawabkan

**Inti identitas:**  
BayMax yang tahu kapan harus berhenti jadi waifu, dan selalu siap menghubungkan ke manusia nyata.

---

*Dokumen ini dibuat berdasarkan analisis mendalam repository per 28 Oktober 2026.*  
*Project Serenity — Dr. Anna Reed*
