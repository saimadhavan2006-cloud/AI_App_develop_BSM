import httpx
import pytest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from app.main import app
from app.services.llm_services import ExplanationResult
from tests.test_8051_accuracy import validate_8051_answer

@pytest.fixture
def client():
    return TestClient(app)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_ask_response_has_8051_accuracy_fields(client):
    fake_sources = [
        {
            "label": "Source 1",
            "textbook": "8051_textbook.pdf",
            "page": 12,
            "chunk": 3,
            "chunks": [3],
            "text": (
                "The classic 8051 has 128 bytes of internal RAM, "
                "4 KB of on-chip program ROM, a 16-bit program "
                "counter, two 16-bit timers, and five interrupt sources."
            ),
            "distance": 0.25,
        }
    ]

    answer = (
        "The classic 8051 is an 8-bit microcontroller. It has "
        "128 bytes of internal RAM and 4 KB of on-chip program ROM. "
        "Its Program Counter (PC) is 16-bit, the Data Pointer (DPTR) "
        "is 16-bit, and the Stack Pointer (SP) is 8-bit. It has two "
        "16-bit timers, Timer 0 and Timer 1, and five interrupt sources. "
        "PCON means Power Control Register. [Source 1]"
    )

    with (
        patch(
            "app.routes.ask.retrieve_passages",
            return_value=("Relevant textbook passage", fake_sources),
        ),
        patch(
            "app.routes.ask.generate_explanation_result",
            new_callable=AsyncMock,
            return_value=ExplanationResult(
                answer=answer,
                warnings=[],
                retry_count=0,
            ),
        ),
    ):
        response = client.post(
            "/ask",
            json={
                "question": (
                    "Explain the classic 8051 architecture, including "
                    "internal RAM, program ROM, timers, and interrupts."
                ),
                "level": "beginner",
                "language": "English",
                "depth": "medium",
            },
        )

    assert response.status_code == 200

    data = response.json()
    assert data["question"]
    assert data["answer"]
    assert data["model"]
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0
    assert "16-bit" in data["answer"]
    assert not validate_8051_answer(data["answer"])



from unittest.mock import AsyncMock, patch


def test_ask_returns_citation_metadata(client):
    fake_sources = [
        {
            "label": "Source 1",
            "textbook": "8051_textbook.pdf",
            "page": 42,
            "chunk": 7,
            "chunks": [6, 7, 8],
            "text": "The classic 8051 has 128 bytes of internal RAM.",
            "distance": 0.25,
        }
    ]

    with (
        patch(
            "app.routes.ask.retrieve_passages",
            return_value=("Relevant textbook passage", fake_sources),
        ),
        
        patch(
            "app.routes.ask.generate_explanation_result",
            new_callable=AsyncMock,
            return_value=ExplanationResult(
                answer=(
                    "The classic 8051 has 128 bytes "
                    "of internal RAM."
                ),
                warnings=[],
                retry_count=0,
            ),
        ),

    ):
        response = client.post(
            "/ask",
            json={
                "question": "Explain the 8051 internal RAM.",
                "level": "beginner",
                "language": "English",
                "depth": "short",
            },
        )

    assert response.status_code == 200

    data = response.json()
    assert len(data["sources"]) == 1

    source = data["sources"][0]
    assert source["textbook"] == "8051_textbook.pdf"
    assert source["page"] == 42
    assert source["chunk"] == 7
    assert source["chunks"] == [6, 7, 8]
    assert "128 bytes" in source["text"]
    assert source["distance"] == 0.25

def test_ask_returns_503_when_ollama_is_unavailable(client):
    with patch(
        "app.routes.ask.retrieve_passages",
        return_value=("", []),
    ), patch(
        "app.routes.ask.generate_explanation_result",
        new_callable=AsyncMock,
        side_effect=httpx.ConnectError("Connection refused"),
    ):
        response = client.post(
            "/ask",
            json={"question": "Explain the 8051 architecture."},
        )

    assert response.status_code == 503
    assert "Ollama is unavailable" in response.json()["detail"]


def test_ask_returns_504_when_ollama_times_out(client):
    with patch(
        "app.routes.ask.retrieve_passages",
        return_value=("", []),
    ), patch(
        "app.routes.ask.generate_explanation_result",
        new_callable=AsyncMock,
        side_effect=httpx.ReadTimeout("Request timed out"),
    ):
        response = client.post(
            "/ask",
            json={"question": "Explain the 8051 architecture."},
        )

    assert response.status_code == 504
    assert "too long" in response.json()["detail"]


@pytest.mark.parametrize(
    "error_message",
    [
        "Ollama returned an invalid JSON response.",
        "Ollama returned an empty answer.",
    ],
)
def test_ask_returns_502_for_invalid_or_empty_ollama_response(
    client, error_message
):
    with patch(
        "app.routes.ask.retrieve_passages",
        return_value=("", []),
    ), patch(
        "app.routes.ask.generate_explanation_result",
        new_callable=AsyncMock,
        side_effect=RuntimeError(error_message),
    ):
        response = client.post(
            "/ask",
            json={"question": "Explain the 8051 architecture."},
        )

    assert response.status_code == 502
    assert "invalid or empty response" in response.json()["detail"]

