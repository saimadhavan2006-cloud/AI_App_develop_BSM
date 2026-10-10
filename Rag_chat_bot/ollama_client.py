import requests
ollama_url = "http://localhost:11434/api/generate"
model_name = "llama3.2:latest"
def ask_ollama(prompt):
    response = requests.post(
        ollama_url,
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]