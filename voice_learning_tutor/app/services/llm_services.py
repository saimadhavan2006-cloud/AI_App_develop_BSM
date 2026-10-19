import re
from app.services.accuracy_validator import validate_8051_answer
import httpx
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:latest"

from dataclasses import dataclass
@dataclass
class ExplanationResult:
    answer: str
    warnings: list[str]
    retry_count: int


async def generate_explanation_result(
    question: str,
    level: str = "beginner",
    language: str = "English",
    depth: str = "medium",
    context: str = ""
) -> ExplanationResult:
    if context.strip():
        source_instructions = f"""
Use the retrieved textbook passages as evidence.
Do not invent citations or unsupported textbook claims.
Distinguish internal RAM, program memory, external memory,
and SFR address space.
Treat OCR errors cautiously.
Explain source conflicts if present.

Classic 8051 accuracy:
- Internal RAM: 128 bytes.
- On-chip program ROM: 4 KB; variants differ.
- Four register banks, eight registers per bank.
- Timer 0 is T0; Timer 1 is T1.
- Five interrupt sources: INT0, Timer 0, INT1, Timer 1, serial.
- SFRs are separate from general-purpose RAM.
- Harvard architecture has separate code and data spaces.

TEXTBOOK PASSAGES:
{context}
"""
    else:
        source_instructions = """
    No textbook passages were retrieved.
    Textbook verification is unavailable; do not invent citations.
    """

    prompt = f"""
    You are a friendly, technically accurate educational tutor.

    Student level: {level}
    Language: {language}
    Depth: {depth}

    {source_instructions}

    Question: {question}

    Answer clearly with relevant headings and concise bullet points.
    Avoid repetition and unsupported claims.
    Answer in {language}.
    """

    is_8051_question = bool(
        re.search(r"\b8051\b", question, re.IGNORECASE)
    )


    async def call_ollama(current_prompt: str) -> str:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": current_prompt,
            "stream": False,
            "options": {"temperature": 0.2},
        }

        timeout = httpx.Timeout(
            300.0,
            connect=5.0,
            pool=10.0,
        )

        prompt_chars = len(current_prompt)
        print(f"LLM prompt size: {prompt_chars:,} characters")
        request_start = time.perf_counter()

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            try:
                data = response.json()
            except ValueError as exc:
                raise RuntimeError(
                    "Ollama returned an invalid JSON response."
                ) from exc

            if not isinstance(data, dict):
                raise RuntimeError(
                    "Ollama returned an unexpected response format."
                )

        elapsed = time.perf_counter() - request_start
        answer_text = data.get("response", "").strip()

        print(f"Ollama request took: {elapsed:.2f}s")
        print(f"LLM answer size: {len(answer_text):,} characters")

        if not answer_text:
            raise RuntimeError("Ollama returned an empty answer.")

        return answer_text



    print("Starting initial generation...")
    answer = await call_ollama(prompt)
    print("Initial generation completed.")

    warnings: list[str] = []
    retry_count = 0
    max_retries = 2

    if is_8051_question:
        while True:
            validation_start = time.perf_counter()
            issues = validate_8051_answer(answer, question)

            print(
                f"Validation took: "
                f"{time.perf_counter() - validation_start:.2f}s"
            )
            print("8051 validation issues:", issues)

            if not issues or retry_count >= max_retries:
                warnings = issues
                break

            retry_count += 1
            print(f"Retrying generation ({retry_count}/{max_retries})...")

            retry_prompt = f"""{prompt}

Your previous answer has these technical issues:
{chr(10).join("- " + issue for issue in issues)}

Rewrite the complete answer. Correct every listed issue.
Do not repeat incorrect claims. Use the retrieved textbook
passages as evidence and do not invent citations.

PREVIOUS ANSWER:
{answer}
"""

            answer = await call_ollama(retry_prompt)

        if warnings:
            print("WARNING: Validation issues remain:", warnings)


    return ExplanationResult(
        answer=answer,
        warnings=warnings,
        retry_count=retry_count,
    )


async def generate_explanation(
    question: str,
    level: str = "beginner",
    language: str = "English",
    depth: str = "medium",
    context: str = "",
) -> str:
    result = await generate_explanation_result(
        question=question,
        level=level,
        language=language,
        depth=depth,
        context=context,
    )
    return result.answer
