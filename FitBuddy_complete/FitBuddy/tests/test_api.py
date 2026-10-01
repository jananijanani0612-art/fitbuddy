import os
from pathlib import Path

TEST_DB = Path("/tmp/fitbuddy_test.db")
if TEST_DB.exists():
    TEST_DB.unlink()

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_plan():
    response = client.post("/api/plans", json={
        "name": "Test User",
        "age": 25,
        "weight_kg": 65,
        "goal": "general wellness",
        "intensity": "medium",
        "experience": "beginner",
        "equipment": "home",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] >= 1
    assert len(data["plan"]["days"]) == 7
    assert data["source"] == "fallback"


def test_get_plan():
    response = client.get("/api/plans/1")
    assert response.status_code == 200
    assert response.json()["plan"]["title"]


def test_feedback():
    response = client.post("/api/plans/1/feedback", json={
        "feedback": "Please add more cardio and include more rest days."
    })
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_tip():
    response = client.get("/api/tips", params={"goal": "muscle gain"})
    assert response.status_code == 200
    assert response.json()["tip"]


def test_validation():
    response = client.post("/api/plans", json={
        "name": "A",
        "age": 10,
        "weight_kg": 5,
        "goal": "unknown",
        "intensity": "medium",
    })
    assert response.status_code == 422
