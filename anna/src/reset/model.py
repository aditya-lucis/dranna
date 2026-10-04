# anna/src/reset/model.py — model default keluarga, tanpa API uzur
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage


def buat_anna(temperatur: float = 0.4):
    """init_chat_model: cara standar LangChain v1.x — provider dari string, satu pintu."""
    return init_chat_model(
        "google_genai:gemini-2.5-flash",
        temperature=temperatur,
        max_retries=2,
    )


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY"):
        print("[INFO] Lewati eksekusi live model: GOOGLE_API_KEY belum disetel di .env")
    else:
        anna = buat_anna()
        r = anna.invoke([HumanMessage(content="sapa singkat: 'hai anna'")])
        print("Respons Anna:", r.content[:80])
