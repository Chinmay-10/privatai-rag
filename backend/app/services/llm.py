
import requests
from app.core.config import settings


def call_ollama(prompt: str) -> str:
    """
    Robust, blocking call to local Ollama LLM.
    """
    try:
        response = requests.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except Exception:
        return "LLM service unavailable."
