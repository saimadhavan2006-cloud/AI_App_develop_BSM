import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:latest"


async def generate_explanation(
    question: str,
    level: str = "beginner",
    language: str = "English",
    depth: str = "medium"
) -> str:

    prompt = f"""
You are a friendly educational tutor.

Explain the following question clearly.
Use examples when helpful.

Student level: {level}
Preferred language: {language}
Explanation depth: {depth}

Question: {question}
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.4}
    }

    timeout = httpx.Timeout(180.0, connect=5.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()

    answer = data.get("response", "").strip()

    if not answer:
        raise RuntimeError("Ollama returned an empty answer.")

    return answer
