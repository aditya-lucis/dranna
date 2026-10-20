# anna/src/piii/node_rujuk.py — node rujuk di graph (geo-aware, diverifikasi)
from anna.src.piii.rujuk import kalimat_rujuk


def node_rujuk(state: dict) -> dict:
    geo = state.get("geo", "id")
    sinyal = state.get("sinyal_rujuk", "")
    nama = state.get("nama", "kamu")
    return {
        **state,
        "messages": [
            {
                "role": "assistant",
                "content": kalimat_rujuk(sinyal=sinyal, geo=geo, nama=nama),
            }
        ],
    }
