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
TEXTBOOK EVIDENCE AND CITATION RULES

The retrieved context contains source labels such as [Source 1].
Use only the source labels that actually appear in that context.

1. Cite textbook-supported factual claims with the relevant label,
   for example: "The 8051 has 128 bytes of internal RAM [Source 1]."
2. Place citations immediately after the claim they support.
3. Cite each distinct claim with the source that supports it.
4. Do not invent source labels, textbook titles, page numbers,
   quotations, or references.
5. Use only facts supported by the retrieved passages when
   describing what the textbooks say.
6. If the passages do not establish a fact, say that the retrieved
   textbooks do not verify it. You may give general background
   separately, clearly labelled as general knowledge.
7. Treat OCR errors cautiously. Do not silently treat unclear text
   as reliable evidence.
8. If sources conflict, describe the conflict rather than guessing.
9. Do not cite a source merely because it discusses the same topic;
   it must support the specific claim.
10. Keep the answer useful for the student's requested level and depth.

8051 accuracy guidance:
- Internal RAM: 128 bytes in the classic 8051.
- On-chip program ROM: 4 KB in the classic 8051; variants differ.
- Four register banks, with eight registers per bank.
- Timer 0 uses T0; Timer 1 uses T1.
- Five interrupt sources in the classic 8051: INT0, Timer 0,
  INT1, Timer 1, and serial.
- SFRs are separate from general-purpose internal RAM.
- Harvard architecture uses separate code and data address spaces.

TEXTBOOK PASSAGES:
{context}
"""
    else:
        source_instructions = """
TEXTBOOK EVIDENCE STATUS

No textbook passages were retrieved for this question.

- Do not claim that the answer is verified by the user's textbooks.
- Do not invent source labels, textbook names, page numbers, or quotes.
- You may answer from general knowledge when reasonably confident.
- Clearly state when textbook verification is unavailable.
- If the question requires specific textbook evidence, explain that
  no supporting passages were found.
"""

    prompt = f"""
You are a friendly, technically accurate educational tutor.

Student level: {level}
Language: {language}
Depth: {depth}

{source_instructions}

Question: {question}

Answer requirements:
- Answer in {language}.
- Use clear headings and concise bullet points where useful.
- Cite textbook-supported claims immediately using [Source N].
- Use only source labels supplied in the retrieved passages.
- Never fabricate citations or imply unsupported claims are verified.
- If evidence is incomplete, clearly explain the limitation.
- Avoid repetition and distinguish general knowledge from textbook evidence.
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
