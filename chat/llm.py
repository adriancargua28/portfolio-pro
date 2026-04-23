import os
import time
import json
import requests
from .models import AVAILABLE_MODELS, DEFAULT_MODEL


NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def get_llm_response(messages, model=DEFAULT_MODEL, stream=False):
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
        "stream": stream,
    }

    start_time = time.time()
    try:
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=60, stream=stream)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "content": f"Error al conectar con el modelo: {str(e)}",
            "tokens": 0,
            "response_time_ms": int((time.time() - start_time) * 1000),
        }

    elapsed = int((time.time() - start_time) * 1000)

    if stream:
        return response  # Return raw response for streaming

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    tokens = data.get("usage", {}).get("total_tokens", 0)

    return {
        "content": content,
        "tokens": tokens,
        "response_time_ms": elapsed,
    }


def get_llm_stream(messages, model=DEFAULT_MODEL):
    """Generator that yields SSE-formatted token chunks."""
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
        "stream": True,
    }

    try:
        with requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=60, stream=True) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data["choices"][0].get("delta", {})
                            token = delta.get("content", "")
                            if token:
                                yield f"data: {json.dumps({'token': token})}\n\n"
                        except (json.JSONDecodeError, KeyError):
                            continue
    except requests.exceptions.RequestException as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"


def get_available_models():
    return AVAILABLE_MODELS
