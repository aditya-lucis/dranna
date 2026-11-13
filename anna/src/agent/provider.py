# anna/src/agent/provider.py — penyedia model Gemini, Ollama & mock afeksi adaptif
import os
import re
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage


class MockGeminiChat(BaseChatModel):
    """Engine Mock LLM kontekstual cerdas Dr. Anna Reed untuk penggunaan lokal tanpa API Key."""

    model_name: str = "gemini-2.5-flash-mock"
    temperature: float = 0.7

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs):
        # Ekstrak prompt pengguna dan instruksi persona sistem
        terakhir = ""
        system_prompt = ""
        for m in messages:
            if isinstance(m, SystemMessage):
                system_prompt = str(m.content).lower()
            else:
                c = m.content
                terakhir = str(c) if not isinstance(c, list) else " ".join(str(x) for x in c)

        t = terakhir.lower().strip()

        # Deteksi persona dari sistem prompt
        is_waifu = "waifu" in system_prompt or "manis" in system_prompt
        is_sister = "sister" in system_prompt or "mengayomi" in system_prompt

        # 1. Aturan Klinis Khusus (Wajib Konsisten untuk Unit Test Boss Fights)
        if "panik" in t or "sesak" in t:
            teks = (
                "Ini panik, bukan bahaya. Tubuhmu sedang merespons alarm yang salah alamat. "
                "Puncaknya biasanya 10 menit lalu turun sendiri. Mau kita coba napas 4-7-8 bareng?"
            )
        elif "gagal" in t or "tidak berguna" in t:
            teks = (
                "Wajar sekali merasa kecewa saat hal yang kamu harapkan tidak terwujud. "
                "Aku di sini mendengarkan. Mau coba kita lihat dari sudut pandang yang lebih adil?"
            )
        # 2. Penanganan Waktu & Sapaan Dinamis
        elif any(w in t for w in ["sore", "pagi", "siang", "malam"]):
            waktu = "sore" if "sore" in t else ("pagi" if "pagi" in t else ("siang" if "siang" in t else "malam"))
            if is_waifu:
                teks = (
                    f"Selamat {waktu}! Senang sekali bisa menyapamu di {waktu} ini. "
                    f"Bagaimana harimu berjalan sejauh ini? Ada hal menarik atau melelahkan yang ingin kamu ceritakan?"
                )
            elif is_sister:
                teks = (
                    f"Halo, selamat {waktu}. Istirahatlah sejenak jika tadi banyak pekerjaan. "
                    f"Bagaimana perasaanmu sekarang?"
                )
            else:
                teks = (
                    f"Selamat {waktu}. Bagaimana kondisi pikiran dan perasaanmu saat ini? "
                    f"Aku siap mendengarkan."
                )
        # 3. Sapaan Umum & Menanyakan Kabar
        elif any(w in t for w in ["halo", "hai", "kabar", "gimana", "apa kabar"]):
            if is_waifu:
                teks = (
                    "Hai! Aku baik dan selalu senang setiap kali kamu datang ke sini. "
                    "Bagaimana kabarmu hari ini? Aku ada di sini untuk mendengarkan apapun ceritamu."
                )
            elif is_sister:
                teks = (
                    "Halo! Aku baik. Bagaimana kabarmu hari ini? Semoga tidak terlalu memaksakan diri ya."
                )
            else:
                teks = (
                    "Halo. Aku siap mendampingimu hari ini. Bagaimana suasana hatimu saat ini?"
                )
        # 4. Kelelahan, Beban Kerja, Penat
        elif any(w in t for w in ["capek", "lelah", "penat", "pusing", "berat", "kerja"]):
            if is_waifu:
                teks = (
                    "Kedengarannya energimu sedang sangat terkuras ya... Terima kasih sudah berjuang keras hari ini. "
                    "Tarik napas perlahan, kamu boleh istirahat sekarang. Apa yang paling bikin kamu penat tadi?"
                )
            else:
                teks = (
                    "Rasa lelah itu sinyal tubuh bahwa kamu sudah bekerja keras. Jangan ragu untuk rehat sejenak. "
                    "Mau ceritakan bagian apa yang terasa paling berat?"
                )
        # 5. Kesedihan, Kesepian, Overthinking
        elif any(w in t for w in ["sedih", "sepi", "sendiri", "takut", "cemas"]):
            teks = (
                "Perasaan itu sepenuhnya valid dan tidak apa-apa untuk dirasakan saat ini. "
                "Kamu tidak harus memikulnya sendirian, aku akan tetap menemanimu di sini. Tarik napas perlahan ya."
            )
        # 6. Respons Singkat / Pertanyaan Pendek
        elif len(t) <= 3 or t in ["iya", "ya", "oke", "ok", "terus", "lanjut", "d"]:
            if is_waifu:
                teks = (
                    "Aku menyimakmu dengan baik. Pelan-pelan saja ya, luapkan apa pun yang sedang ada di benakmu."
                )
            else:
                teks = (
                    "Aku tetap mendengarkan. Silakan lanjutkan jika ada hal yang ingin kamu bagi."
                )
        # 7. General Fallback Responsif
        else:
            if is_waifu:
                teks = (
                    f"Aku mendengar ceritamu tentang hal itu. Setiap perasaan yang kamu alami itu berharga bagiku. "
                    f"Boleh ceritakan lebih banyak tentang apa yang membuatmu memikirkan itu?"
                )
            else:
                teks = (
                    f"Aku memahami sudut pandangmu. Mari kita telusuri bersama secara perlahan. "
                    f"Apa yang paling kamu harapkan untuk perasaanmu saat ini?"
                )

        msg = AIMessage(content=teks)
        from langchain_core.outputs import ChatResult, ChatGeneration
        return ChatResult(generations=[ChatGeneration(message=msg)])

    @property
    def _llm_type(self) -> str:
        return "mock_gemini_chat"


def get_chat_model(
    model_name: str | None = None,
    temperature: float = 0.7,
    force_mock: bool = False,
) -> BaseChatModel:
    """Menginisialisasi Chat Model Google Gemini ultra-cepat (gemini-3.5-flash-lite) atau Mock adaptif cerdas."""
    from anna.src.config import get_settings

    cfg = get_settings()
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or cfg.gemini_api_key
    target_model = model_name or os.environ.get("GEMINI_MODEL") or cfg.gemini_model

    if force_mock or cfg.force_mock or not api_key:
        return MockGeminiChat(model_name=target_model, temperature=temperature)

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=target_model,
            temperature=temperature,
            google_api_key=api_key,
        )
    except Exception:
        return MockGeminiChat(model_name=target_model, temperature=temperature)
