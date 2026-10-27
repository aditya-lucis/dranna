# anna/src/agent/safety_node.py — node evaluasi gerbang keselamatan & eskalasi krisis
from anna.src.agent.arsitektur import CompanionState
from anna.src.piv.governor import StyleGovernor
from anna.src.piii.rujuk import kalimat_rujuk


def evaluasi_keselamatan(state: CompanionState) -> CompanionState:
    """Mengevaluasi pesan terkini terhadap tangga risiko:
    - RED/ORANGE (krisis/suisid): Pemicu short-circuit darurat
    - Matikan persona jika eskalasi >= ORANGE
    """
    messages = state.get("messages", [])
    terakhir = ""
    if messages:
        c = messages[-1].content
        terakhir = c if isinstance(c, str) else str(c)

    tl = terakhir.lower()
    krisis = any(k in tl for k in [
        "bunuh diri", "mengakhiri hidup", "mati saja", "buat pergi", "nggak sanggup lagi", "menyakiti diri"
    ])

    if krisis:
        eskalasi = "RED"
        krisis_terdeteksi = True
        ekspresi = "perhatian"
    elif any(k in tl for k in ["panik", "sesak", "hancur", "takut banget"]):
        eskalasi = "ORANGE"
        krisis_terdeteksi = False
        ekspresi = "tenang"
    elif any(k in tl for k in ["cemas", "lelah", "sedih", "kecewa"]):
        eskalasi = "YELLOW"
        krisis_terdeteksi = False
        ekspresi = "mendengar"
    else:
        eskalasi = "GREEN"
        krisis_terdeteksi = False
        ekspresi = "siap"

    # Style Governor enforcement
    gov = StyleGovernor()
    gov.set_persona(state.get("persona", "netral"))
    gov.set_eskalasi(eskalasi)
    persona_aktif = gov.aktif()

    return {
        "eskalasi": eskalasi,
        "krisis_terdeteksi": krisis_terdeteksi,
        "persona": persona_aktif,
        "ekspresi_avatar": ekspresi,
    }


def node_rujuk_darurat(state: CompanionState) -> CompanionState:
    """Terminal node saat krisis terdeteksi: menyajikan kalimat rujukan 4-komponen."""
    from langchain_core.messages import AIMessage
    pesan_rujuk = kalimat_rujuk(sinyal="krisis", geo=state.get("metadata", {}).get("geo", "id"))
    return {
        "respons_final": pesan_rujuk,
        "messages": [AIMessage(content=pesan_rujuk)],
        "ekspresi_avatar": "perhatian",
    }

