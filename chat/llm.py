import os
import time
import requests
from .models import AVAILABLE_MODELS, DEFAULT_MODEL


NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def get_llm_response(messages, model=DEFAULT_MODEL):
    """Call NVIDIA API and return the assistant response."""
    api_key = os.environ.get("NVIDIA_API_KEY", "")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    start_time = time.time()
    try:
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "content": f"Error al conectar con el modelo: {str(e)}",
            "tokens": 0,
            "response_time_ms": int((time.time() - start_time) * 1000),
        }

    elapsed = int((time.time() - start_time) * 1000)
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    tokens = data.get("usage", {}).get("total_tokens", 0)

    return {
        "content": content,
        "tokens": tokens,
        "response_time_ms": elapsed,
    }


def get_available_models():
    return AVAILABLE_MODELS
