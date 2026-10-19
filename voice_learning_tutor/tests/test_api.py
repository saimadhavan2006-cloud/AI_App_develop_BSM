
from app.services.llm_services import ExplanationResult

import pytest
from fastapi.testclient import TestClient
from app.main import app
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
    print("\n========== GENERATED 8051 ANSWER ==========")
    print(data["answer"])
    issues = validate_8051_answer(data["answer"])
    assert not issues, (
        "8051 answer contains possible accuracy issues:\n"
        + "\n".join(issues)
    )


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

