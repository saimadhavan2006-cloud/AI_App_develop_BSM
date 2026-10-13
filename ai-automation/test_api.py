from fastapi.testclient import TestClient
from app import app

def test_api():
    with TestClient(app) as client:

        response = client.get("/")
        assert response.status_code == 200

        response = client.get("/health")
        assert response.status_code == 200

        response = client.post(
            "/analyse",
            json={"text": "I love this product! It is excellent."},
        )
        assert response.status_code == 200

        result = response.json()
        assert result["sentiment"] == "POSITIVE"
        assert 0 <= result["confidence"] <= 1
        assert result["suggested_action"] == "Record as positive feedback"
        print("Positive result:", result)

        response = client.post(
            "/analyse",
            json={"text": "This product is terrible. I hate it."},
        )
        assert response.status_code == 200

        result = response.json()
        assert result["sentiment"] == "NEGATIVE"
        assert result["suggested_action"] == (
            "Flag for customer support review"
        )
        print("Negative result:", result)

        for text in ["", "   "]:
            response = client.post("/analyse", json={"text": text})
            assert response.status_code == 422

        response = client.post("/analyse", json={})
        assert response.status_code == 422

        response = client.post(
            "/analyse",
            json={"text": "A" * 5001},
        )
        assert response.status_code == 422

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_api()
