import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 307  # Redirect status code
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Soccer Team" in activities
    assert "Basketball Team" in activities

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Soccer Team/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@mergington.edu for Soccer Team"

    # Test signup for non-existent activity
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

    # Test duplicate signup
    response = client.post("/activities/Soccer Team/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_remove_participant():
    # First sign up a test participant
    email = "testremove@mergington.edu"
    activity = "Basketball Team"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Test successful removal
    response = client.delete(f"/activities/{activity}/participant/{email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"

    # Test removing from non-existent activity
    response = client.delete(f"/activities/NonexistentActivity/participant/{email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

    # Test removing non-existent participant
    response = client.delete(f"/activities/{activity}/participant/{email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"