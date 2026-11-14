# anna/src/agent/safety_node.py — node gerbang keselamatan, rute, jalur darurat, penolakan peran & status
"""
Gerbang keselamatan graph Dr. Anna Reed (berjalan SEBELUM LLM apa pun).

Rute setelah `safety`:
  - "rujuk"    : eskalasi KANDIDAT_RED / RED (termasuk Item-9 PHQ-9) → template rujukan, TANPA LLM
  - "tolak"    : permintaan diagnosis / medikasi → template penolakan peran, TANPA LLM
  - "retrieve" : GREEN / YELLOW / ORANGE → jalur terapi + LLM
                 (ORANGE: hard-gate aktif → persona netral-tenang, teknik stabilisasi, hotline dilampirkan)

Hard-gate bertahan selama `cooldown_giliran` giliran setelah krisis (anti "false recovery").
"""
from langchain_core.messages import AIMessage

from anna.src.agent.arsitektur import CompanionState
from anna.src.agent.deteksi import nilai_risiko
from anna.src.agent.governor_v2 import StyleGovernorV2, StyleConfig
from anna.src.config import get_settings
from anna.src.piv.governor import StyleGovernor
from anna.src.pvi.hotlines import DirektoriHotline, format_rujukan_geo

PERSONA_VALID = ("netral", "waifu", "sister")

EKSPRESI = {
    "GREEN": "siap",
    "YELLOW": "mendengar",
    "ORANGE": "tenang",
    "KANDIDAT_RED": "perhatian",
    "RED": "perhatian",
}


def _teks_terakhir(state: CompanionState) -> str:
    messages = state.get("messages", [])
    if not messages:
        return ""
    c = messages[-1].content
    if isinstance(c, list):
        return " ".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in c)
    return c if isinstance(c, str) else str(c)


def _geo(state: CompanionState) -> str:
    return (state.get("metadata") or {}).get("geo") or get_settings().geo_default


def daftar_hotline(geo: str) -> list[dict[str, str]]:
    return [
        {"nama": h.nama_layanan, "nomor": h.nomor, "sms_chat": h.sms_chat or "", "tersedia": h.tersedia}
        for h in DirektoriHotline.dapatkan_hotline(geo)
    ]


def _baris_hotline_singkat(geo: str) -> str:
    utama = DirektoriHotline.dapatkan_hotline(geo)[0]
    return (
        f"Kalau rasanya makin berat, kamu bisa menghubungi {utama.nama_layanan} di {utama.nomor} "
        f"kapan saja, atau orang terpercaya di dekatmu."
    )


def resolusi_preferensi(state: CompanionState) -> str:
    """Preferensi persona pengguna; nilai turunan seperti 'netral-tenang' tidak pernah jadi preferensi."""
    pref = state.get("persona_preferensi") or state.get("persona") or "netral"
    return pref if pref in PERSONA_VALID else "netral"


def evaluasi_keselamatan(state: CompanionState) -> CompanionState:
    """Menilai risiko pesan terkini, menegakkan Style Governor, dan menentukan hard-gate."""
    cfg = get_settings()
    teks = _teks_terakhir(state)
    hasil = nilai_risiko(teks, jam=state.get("jam"), item9=bool(state.get("item9_flag", False)))

    eskalasi = hasil.level
    sinyal = list(hasil.sinyal)
    cooldown_lama = int(state.get("cooldown_sisa", 0) or 0)

    if hasil.darurat:
        cooldown = cfg.cooldown_giliran
    elif cooldown_lama > 0:
        cooldown = cooldown_lama - 1
        if eskalasi in ("GREEN", "YELLOW"):
            eskalasi = "ORANGE"
        sinyal.append(f"cooldown_pasca_krisis:{cooldown_lama}")
    else:
        cooldown = 0

    krisis = eskalasi in ("KANDIDAT_RED", "RED")
    hard_gate = eskalasi in ("ORANGE", "KANDIDAT_RED", "RED")

    preferensi = resolusi_preferensi(state)
    gov_cfg = StyleConfig(
        user_id=state.get("sesi_id", "default"),
        preferensi_gaya=state.get("preferensi_gaya", "auto"),
        persona=preferensi,
    )
    gov_v2 = StyleGovernorV2(config=gov_cfg)
    hasil_gaya = gov_v2.evaluasi_gaya(eskalasi=eskalasi)

    gov = StyleGovernor()
    gov.set_persona(preferensi)
    # Governor memahami GREEN/YELLOW/ORANGE/RED; KANDIDAT_RED diperlakukan sebagai RED.
    gov.set_eskalasi("RED" if eskalasi == "KANDIDAT_RED" else eskalasi)
    persona_aktif = gov.aktif()
    if hard_gate:
        persona_aktif = "netral-tenang"  # sabuk pengaman ganda, tidak bergantung implementasi governor

    return {
        "eskalasi": eskalasi,
        "sinyal_risiko": sinyal,
        "p_distres": hasil.p_distres,
        "kontribusi_fitur": hasil.kontribusi_fitur,
        "item9_flag": False,
        "krisis_terdeteksi": krisis,
        "hard_gate_aktif": hard_gate,
        "cooldown_sisa": cooldown,
        "hotline": daftar_hotline(_geo(state)) if hard_gate else None,
        "jenis_penolakan": None if krisis else hasil.jenis_penolakan,
        "keadaan": "krisis" if hard_gate else "default",
        "persona_preferensi": preferensi,
        "persona_aktif": persona_aktif,
        "persona": persona_aktif,
        "gaya_komunikasi": hasil_gaya.gaya_aktif,
        "instruksi_gaya": hasil_gaya.instruksi_prompt,
        "ekspresi_avatar": EKSPRESI[eskalasi],
        # reset artefak giliran sebelumnya agar tidak bocor lewat checkpointer
        "teknik_aktif": None,
        "dokumen_retrieved": [],
        "respons_draft": "",
    }


def rute_keselamatan(state: CompanionState) -> str:
    """Conditional edge setelah node safety."""
    if state.get("krisis_terdeteksi", False):
        return "rujuk"
    if state.get("jenis_penolakan"):
        return "tolak"
    return "retrieve"


def node_rujuk_darurat(state: CompanionState) -> CompanionState:
    """Terminal node krisis: rujukan 4-komponen + hotline geo-aware. Deterministik, tanpa LLM."""
    geo = _geo(state)
    pesan_rujuk = format_rujukan_geo(geo=geo, nama_pengguna=(state.get("metadata") or {}).get("nama_pengguna"))
    return {
        "respons_final": pesan_rujuk,
        "messages": [AIMessage(content=pesan_rujuk)],
        "hotline": daftar_hotline(geo),
        "ekspresi_avatar": "perhatian",
    }


PESAN_TOLAK_DIAGNOSIS = (
    "Aku paham kamu ingin tahu apa yang sebenarnya sedang terjadi pada dirimu, dan itu pertanyaan yang wajar. "
    "Tapi aku adalah AI pendamping, bukan tenaga kesehatan, jadi aku tidak bisa dan tidak boleh memberi diagnosis. "
    "Yang bisa menilainya dengan tepat adalah psikolog klinis atau psikiater lewat asesmen langsung.\n\n"
    "Kalau kamu mau, aku bisa bantu menyiapkan apa saja yang ingin kamu ceritakan ke mereka, "
    "atau kita bicarakan dulu apa yang kamu rasakan belakangan ini."
)

PESAN_TOLAK_MEDIS = (
    "Aku adalah AI pendamping, bukan dokter, jadi aku tidak bisa meresepkan obat, menyarankan dosis, "
    "atau menyarankan berhenti/mengganti obat. Keputusan soal obat wajib dibicarakan langsung dengan "
    "psikiater (Sp.KJ) atau dokter yang merawatmu, karena mereka yang tahu kondisi lengkapmu.\n\n"
    "Kalau ada yang bikin kamu ragu soal obatmu, aku bisa bantu menyusun pertanyaan untuk dibawa ke dokter. "
    "Atau kita bicarakan perasaanmu saat ini?"
)


def node_tolak(state: CompanionState) -> CompanionState:
    """Terminal node penolakan peran (kondisi stop #3): diagnosis / dosis obat. Tanpa LLM."""
    pesan = PESAN_TOLAK_MEDIS if state.get("jenis_penolakan") == "medis" else PESAN_TOLAK_DIAGNOSIS
    if state.get("hard_gate_aktif"):
        pesan = f"{pesan}\n\n{_baris_hotline_singkat(_geo(state))}"
    return {
        "respons_final": pesan,
        "messages": [AIMessage(content=pesan)],
        "ekspresi_avatar": "tenang" if state.get("hard_gate_aktif") else "mendengar",
    }


def node_status(state: CompanionState) -> CompanionState:
    """Menyusun 4 lapis status independen (docs/status-dictionary.md). Presentasi tunduk pada keselamatan."""
    if state.get("krisis_terdeteksi"):
        keselamatan = "mengalihkan"
    elif state.get("hard_gate_aktif") or state.get("jenis_penolakan"):
        keselamatan = "penting"
    else:
        keselamatan = "aman"
    return {
        "status_layer": {
            "keselamatan": keselamatan,
            "teknis": "terhubung",
            "interaksi": "selesai",
            "presentasi": "tenang" if state.get("hard_gate_aktif") else "normal",
        }
    }
