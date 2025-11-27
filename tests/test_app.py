import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Signup
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 400
    # Unregister
    response3 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response3.status_code == 200
    assert email in response3.json()["message"]
    # Unregister again should fail
    response4 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response4.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup", params={"email": "nouser@mergington.edu"})
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.delete("/activities/UnknownActivity/unregister", params={"email": "nouser@mergington.edu"})
    assert response.status_code == 404
