import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"


def ask_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=(5, 180),
        )

        response.raise_for_status()

        answer = response.json().get("response", "").strip()

        if not answer:
            raise RuntimeError("Ollama returned an empty response.")

        return answer

    except requests.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. Check that it is running."
        ) from exc

    except requests.Timeout as exc:
        raise RuntimeError(
            "Ollama timed out while generating the response."
        ) from exc