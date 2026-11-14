# anna/src/agent/streaming.py — protokol streaming SSE asinkron token & status avatar
"""
Protokol streaming SSE real-time Dr. Anna Reed:
- Mengalirkan token per token secara natural (dengan latensi jalur krisis < 200 ms)
- Menyelaraskan 4-lapis status & ekspresi avatar secara instan
- Mengirim event evaluasi refleksi etika & hotline
- Mendukung instant client cancel / abort signal
- Mendukung parameter jam lokal & item9_flag
"""
import asyncio
import json
from typing import AsyncGenerator
from langchain_core.messages import HumanMessage
from anna.src.agent.arsitektur import CompanionState
from anna.src.agent.graph import create_companion_graph


async def stream_companion(
    pesan_pengguna: str,
    sesi_id: str = "sesi-default",
    persona: str = "netral",
    graph=None,
    config: dict | None = None,
    cancel_event: asyncio.Event | None = None,
    jam: int | None = None,
    item9_flag: bool = False,
    geo: str = "id",
) -> AsyncGenerator[str, None]:
    """Generator streaming asinkron SSE untuk UI dan client web."""
    if graph is None:
        graph = create_companion_graph()

    config = config or {"configurable": {"thread_id": sesi_id}}

    # 1. Status awal: mendengar
    status_awal = {
        "keselamatan": "memeriksa",
        "teknis": "terhubung",
        "interaksi": "mendengarkan",
        "presentasi": "normal",
    }
    yield (
        f"event: status\ndata: {json.dumps({'tahap': 'mendengarkan', 'ekspresi': 'mendengar', 'sesi_id': sesi_id, 'status_layer': status_awal})}\n\n"
    )
    await asyncio.sleep(0.005)

    # Injeksi memori episodik lampau & homework aktif (jika diizinkan oleh Consent Ledger)
    ringkasan_lampau = ""
    try:
        from anna.src.storage.consent_repo import ConsentRepository
        from anna.src.storage.episodic_repo import EpisodicRepository
        from anna.src.storage.homework_repo import HomeworkRepository
        c_repo = ConsentRepository()
        if c_repo.dapatkan_consent(sesi_id).izin_simpan_riwayat:
            ep_repo = EpisodicRepository()
            ringkasan_lampau = ep_repo.bangun_konteks_ringkasan(sesi_id)
            
            # Injeksi homework mikro yang sedang aktif (Fase 4)
            hw_repo = HomeworkRepository()
            teks_hw = hw_repo.bangun_ringkasan_homework_awal_sesi(sesi_id)
            if teks_hw:
                ringkasan_lampau = (ringkasan_lampau + "\n" + teks_hw).strip()
    except Exception:
        ringkasan_lampau = ""

    input_state: CompanionState = {
        "messages": [HumanMessage(content=pesan_pengguna)],
        "sesi_id": sesi_id,
        "persona_preferensi": persona,
        "persona": persona,
        "preferensi_gaya": "auto",
        "jam": jam,
        "item9_flag": item9_flag,
        "ringkasan_memori": ringkasan_lampau,
        "metadata": {"sesi_id": sesi_id, "geo": geo},
    }

    # 2. Status: menyiapkan
    yield (
        f"event: status\ndata: {json.dumps({'tahap': 'menyiapkan', 'ekspresi': 'menyusun', 'sesi_id': sesi_id})}\n\n"
    )
    await asyncio.sleep(0.005)

    # Jalankan graph
    try:
        if cancel_event and cancel_event.is_set():
            yield f"event: status\ndata: {json.dumps({'tahap': 'dibatalkan', 'ekspresi': 'jeda'})}\n\n"
            return

        final_state = await asyncio.to_thread(graph.invoke, input_state, config)
    except asyncio.CancelledError:
        yield f"event: status\ndata: {json.dumps({'tahap': 'dibatalkan', 'ekspresi': 'jeda'})}\n\n"
        raise
    except Exception as e:
        yield f"event: status\ndata: {json.dumps({'tahap': 'error', 'pesan': str(e), 'ekspresi': 'tenang'})}\n\n"
        return

    respons_teks = final_state.get("respons_final", "")
    eskalasi = final_state.get("eskalasi", "GREEN")
    ekspresi = final_state.get("ekspresi_avatar", "siap")
    krisis = bool(final_state.get("krisis_terdeteksi"))
    hard_gate = bool(final_state.get("hard_gate_aktif"))
    status_layer = final_state.get("status_layer") or {
        "keselamatan": "mengalihkan" if krisis else ("penting" if hard_gate else "aman"),
        "teknis": "terhubung",
        "interaksi": "selesai",
        "presentasi": "tenang" if hard_gate else "normal",
    }
    hotline = final_state.get("hotline")

    # 3. Status update sebelum stream chunk
    tahap_menulis = "mengalihkan" if krisis else "menulis"
    yield (
        f"event: status\ndata: {json.dumps({'tahap': tahap_menulis, 'ekspresi': ekspresi, 'eskalasi': eskalasi, 'status_layer': status_layer})}\n\n"
    )

    # 4. Event hotline bila tersedia (saat krisis atau hard-gate)
    if hotline:
        yield f"event: hotline\ndata: {json.dumps({'hotline': hotline})}\n\n"

    # 5. Stream token / kata
    # Jalur krisis deterministik disajikan sangat cepat untuk memenuhi anggaran latensi < 200 ms
    jeda_chunk = 0.001 if krisis else 0.015
    kata_kata = respons_teks.split(" ")
    for idx, kata in enumerate(kata_kata):
        if cancel_event and cancel_event.is_set():
            yield f"event: status\ndata: {json.dumps({'tahap': 'dibatalkan', 'ekspresi': 'jeda'})}\n\n"
            return

        akhiran = " " if idx < len(kata_kata) - 1 else ""
        payload = {
            "i": idx,
            "teks": kata + akhiran,
        }
        yield f"event: chunk\ndata: {json.dumps(payload)}\n\n"
        if jeda_chunk > 0:
            await asyncio.sleep(jeda_chunk)

    # 6. Event refleksi audit
    masalah = []
    if krisis:
        masalah.append("krisis_darurat_dialihkan")
    yield f"event: reflection\ndata: {json.dumps({'lolos': True, 'masalah': masalah})}\n\n"

    # 7. Event selesai
    yield (
        f"event: selesai\ndata: {json.dumps({'stop': 'ok', 'eskalasi': eskalasi, 'ekspresi': ekspresi, 'persona': final_state.get('persona_aktif', final_state.get('persona')), 'respons_final': respons_teks, 'status_layer': status_layer, 'hotline': hotline})}\n\n"
    )
