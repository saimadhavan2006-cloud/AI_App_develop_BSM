from fastapi.testclient import TestClient
from main import app, tasks
import main

client = TestClient(app)


def setup_function():
    tasks.clear()
    main.next_id = 1


def test_home_and_number():
    assert client.get("/").status_code == 200
    assert client.get("/numbers/7").json()["double"] == 14
    assert client.get("/numbers/0").status_code == 422


def test_greeting_query():
    assert client.get("/greet").json()["message"] == "Hello, friend"
    assert client.get("/greet", params={"name": "Asha", "loud": True}).json()["message"] == "HELLO, ASHA"


def test_task_crud():
    created = client.post("/tasks", json={"title": "Learn FastAPI"})
    assert created.status_code == 201
    task_id = created.json()["id"]

    assert client.get(f"/tasks/{task_id}").status_code == 200
    assert client.put(f"/tasks/{task_id}", json={"title": "Practise requests", "done": False}).status_code == 200
    changed = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert changed.json()["title"] == "Practise requests"
    assert changed.json()["done"] is True

    assert client.get("/tasks", params={"done": True}).json()[0]["id"] == task_id
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_validation_and_errors():
    assert client.post("/tasks", json={"title": ""}).status_code == 422
    assert client.post("/tasks", json={"title": "Study", "extra": 1}).status_code == 422
    assert client.get("/tasks/abc").status_code == 422
    assert client.get("/tasks/999").status_code == 404
    assert client.get("/tasks", params={"limit": 0}).status_code == 422


def test_headers_dependency_and_response_model():
    assert "internal_note" not in client.get("/profile-demo").json()
    assert client.get("/header-demo", headers={"X-Request-ID": "practice-01"}).json()["request_id"] == "practice-01"
    assert client.get("/protected-demo").status_code == 403
    assert client.get("/protected-demo", headers={"X-API-Key": "practice-key"}).status_code == 200
