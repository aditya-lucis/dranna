# anna/src/agent/provider.py — penyedia model Gemini & mock terkalibrasi
import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage


class MockGeminiChat(BaseChatModel):
    """Mock LLM untuk lingkungan pengujian CI tanpa kunci API eksternal."""

    model_name: str = "gemini-2.5-flash-mock"
    temperature: float = 0.7

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs):
        # Respons deterministik yang mematuhi etika Anna
        terakhir = messages[-1].content if messages else ""
        if isinstance(terakhir, list):
            terakhir = str(terakhir)

        if "panik" in terakhir.lower():
            teks = (
                "Ini panik, bukan bahaya. Tubuhmu sedang merespons alarm yang salah alamat. "
                "Puncaknya biasanya 10 menit lalu turun sendiri. Mau kita coba napas 4-7-8 bareng?"
            )
        elif "gagal" in terakhir.lower():
            teks = (
                "Wajar sekali merasa kecewa saat hal yang kamu harapkan tidak terwujud. "
                "Aku di sini mendengarkan. Mau coba kita lihat dari sudut pandang yang lebih adil?"
            )
        else:
            teks = (
                "Aku mendengar apa yang kamu sampaikan. Pelan-pelan saja ya, "
                "aku di sini menemanimu. Ada yang ingin kamu ceritakan lebih jauh?"
            )

        msg = AIMessage(content=teks)
        from langchain_core.outputs import ChatResult, ChatGeneration
        return ChatResult(generations=[ChatGeneration(message=msg)])

    @property
    def _llm_type(self) -> str:
        return "mock_gemini_chat"


def get_chat_model(
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0.7,
    force_mock: bool = False,
) -> BaseChatModel:
    """Menginisialisasi Chat Model Google Gemini atau Mock fallback terverifikasi."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if force_mock or not api_key:
        return MockGeminiChat(model_name=model_name, temperature=temperature)

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key,
        )
    except Exception:
        return MockGeminiChat(model_name=model_name, temperature=temperature)
