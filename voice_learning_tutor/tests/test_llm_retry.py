
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services import llm_services


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_8051_answer_retries_when_validator_finds_issue():
    bad_answer = (
        "The classic 8051 has 128 bytes of internal RAM. "
        "Internal ROM or EPROM of 0 (8031) to 4K (8051)."
    )

    corrected_answer = (
        "The classic 8051 has 128 bytes of internal RAM and "
        "4 KB of on-chip program ROM. Variants differ."
    )

    response_1 = MagicMock()
    response_1.json.return_value = {"response": bad_answer}
    response_1.raise_for_status.return_value = None

    response_2 = MagicMock()
    response_2.json.return_value = {"response": corrected_answer}
    response_2.raise_for_status.return_value = None

    client = MagicMock()
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)
    client.post = AsyncMock(
        side_effect=[response_1, response_2]
    )

    with (
        patch.object(
            llm_services,
            "validate_8051_answer",
            side_effect=[
                ["For the classic 8051, state 4 KB of on-chip program ROM."],
                [],
            ],
        ),
        patch.object(
            llm_services.httpx,
            "AsyncClient",
            return_value=client,
        ),
    ):
        result = await llm_services.generate_explanation(
            question="Explain the classic 8051 architecture.",
            context="Classic 8051 has 128 bytes RAM and 4 KB ROM.",
        )

    assert result == corrected_answer
    assert client.post.await_count == 2
