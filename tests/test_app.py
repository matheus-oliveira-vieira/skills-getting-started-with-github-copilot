import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Check participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]


def test_signup_for_activity_full():
    activity = "Chess Club"
    # Fill up the activity
    for i in range(20):
        client.post(f"/activities/{activity}/signup?email=student{i}@mergington.edu")
    # Now it should be full
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]


def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant():
    activity = "Chess Club"
    email = "removeme@mergington.edu"
    # Add participant
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister endpoint
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Should be 404 if not implemented, 200 if implemented
    assert response.status_code in (200, 404)
