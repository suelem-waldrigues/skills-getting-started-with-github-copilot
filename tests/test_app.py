import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_activity(monkeypatch):
    activity = {
        "description": "Activity used by API tests",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 3,
        "participants": [],
    }
    monkeypatch.setitem(activities, "Test Activity", activity)
    return activity


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_details(client, test_activity):
    # Arrange
    activity_name = "Test Activity"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()[activity_name] == test_activity


def test_signup_adds_participant(client, test_activity):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Test Activity/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up student@mergington.edu for Test Activity"}
    assert test_activity["participants"] == [email]


def test_signup_rejects_duplicate_participant(client, test_activity):
    # Arrange
    email = "student@mergington.edu"
    test_activity["participants"].append(email)

    # Act
    response = client.post(
        "/activities/Test Activity/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }
    assert test_activity["participants"] == [email]


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client, test_activity):
    # Arrange
    email = "student@mergington.edu"
    test_activity["participants"].append(email)

    # Act
    response = client.delete(
        "/activities/Test Activity/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered student@mergington.edu from Test Activity"
    }
    assert test_activity["participants"] == []


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Unknown Activity/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_not_found_for_unregistered_participant(
    client, test_activity
):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Test Activity/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert test_activity["participants"] == []
