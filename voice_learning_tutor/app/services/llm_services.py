
import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:latest"


async def generate_explanation(
    question: str,
    level: str = "beginner",
    language: str = "English",
    depth: str = "medium",
    context: str = ""
) -> str:

    
    if context.strip():
        source_instructions = f"""
        Answer using ONLY the retrieved textbook passages below.

        RETRIEVED TEXTBOOK PASSAGES:
        {context}

        STRICT RULES:
        1. Use only facts explicitly supported by these passages.
        2. Cite claims using the exact labels [Source 1], [Source 2], etc.
        3. Never invent register sizes, pin counts, memory sizes,
           chapter numbers, page numbers, or hardware components.
        4. Preserve the textbook's terminology and meaning.
        5. If OCR text is incomplete or unclear, do not guess the missing text.
        6. Do not add general knowledge, applications, limitations,
           or a conclusion unless the passages support it and it is relevant.
        7. Do not repeat the same facts in multiple sections.
        8. Do not claim that all facts are verified unless you have
           support for each claim in the supplied passages.
        9. If the passages do not provide enough information, state
           exactly which information is missing.
        10. Do not invent details to make the explanation comprehensive.
        11. Do not repeat a list of hardware components in a separate
            Key Features section.
        12. Avoid repeating the same information across sections.
        13. Do not discuss OCR diagram labels unless the student asks
            about the block diagram or those labels are relevant.
        14. Never interpret damaged OCR fragments as confirmed technical
            terms. If a diagram label is unreadable, say it could not
            be reliably extracted instead of guessing its meaning.    

        Write a focused explanation with these sections when supported:
        - CPU and hardware components
        - Memory organization

        Use only sections relevant to the question.
        """

    else:
        source_instructions = """
    No textbook passages were retrieved.
    State that textbook verification is unavailable.
    Do not invent textbook citations.
    """


    prompt = f"""
You are a friendly and accurate educational tutor.

Explain the student's question clearly at the requested level.
Use headings, examples, and bullet points when helpful.

Student level: {level}
Preferred language: {language}
Explanation depth: {depth}

{source_instructions}

QUESTION:
{question}

FINAL CHECK:
- Are the technical claims supported by the cited passages?
- Are all source labels valid?
- Have you avoided invented chapter and page numbers?
- Does the answer contradict any limitation stated in it?
- Have you separated textbook-supported facts from unverified
  additional knowledge?

Answer in {language}.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    timeout = httpx.Timeout(180.0, connect=5.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            OLLAMA_URL,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

    answer = data.get("response", "").strip()

    if not answer:
        raise RuntimeError("Ollama returned an empty answer.")

    return answer
