
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.llm_services import generate_explanation_result


def run_test(question, context):
    answer = (
        "The classic 8051 has 128 bytes of internal RAM [Source 1]."
        if context
        else "Textbook verification is unavailable; this is a general explanation."
    )

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"response": answer}

    mock_client = MagicMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = False
    mock_client.post = AsyncMock(return_value=mock_response)

    with patch(
        "app.services.llm_services.httpx.AsyncClient",
        return_value=mock_client,
    ):
        result = asyncio.run(
            generate_explanation_result(
                question=question,
                context=context,
            )
        )

    prompt = mock_client.post.call_args.kwargs["json"]["prompt"]
    return result, prompt


def test_prompt_requires_citations_for_retrieved_evidence():
    context = (
        "[Source 1]\n"
        "Textbook: 8051.pdf\n"
        "PDF page: 12\n"
        "Chunks included: [3]\n"
        "Passage:\n"
        "The classic 8051 has 128 bytes of internal RAM."
    )

    result, prompt = run_test(
        "Explain 8051 internal RAM.",
        context,
    )

    assert "[Source 1]" in prompt
    assert "Do not invent source labels" in prompt
    assert "PDF page: 12" in prompt
    assert "[Source 1]" in result.answer


def test_prompt_discloses_missing_textbook_evidence():
    result, prompt = run_test(
        "Explain a microcontroller.",
        "",
    )

    assert "No textbook passages were retrieved" in prompt
    assert "Do not invent source labels" in prompt
    assert "Textbook verification is unavailable" in result.answer

