# anna/src/pi/preferensi.py — preferensi eksplisit sebagai penentu utama gaya
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

# Governor gaya: preferensi eksplisit >> estimasi big five >> default netral
LAMBDA_ESTIMASI = 0.0  # Mulai dari 0: Anna TIDAK menebak sampai pengguna setuju

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Kamu Dr. Anna Reed. GAYA saat ini: {gaya}. Jika gaya 'auto', tanyakan "
     "SEKALI di awal relasi: 'Mau aku jadi pendengar yang tenang, teman "
     "yang ringan, atau pendamping yang terstruktur? Kamu bisa ganti "
     "kapan saja.' Hormati pilihan itu sepenuhnya; jangan 'koreksi' "
     "pilihan pengguna dengan asumsi kepribadianmu."),
    ("human", "{pesan}"),
])


def buat_anna(gaya: str = "auto", temperatur: float = 0.4):
    """Membuat runnable Anna dengan gaya preferensi terpasang."""
    model = init_chat_model(
        "google_genai:gemini-2.5-flash",
        temperature=temperatur,
        max_retries=2,
    )
    return PROMPT | model
