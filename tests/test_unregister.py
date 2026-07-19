from urllib.parse import quote

from src import app as app_module


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = app_module.activities[activity_name]["participants"][0]
    encoded_activity = quote(activity_name, safe="")
    encoded_email = quote(existing_email, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants/{encoded_email}")

    # Assert
    assert response.status_code == 200
    assert existing_email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    unknown_activity = quote("Unknown Club", safe="")
    encoded_email = quote("student@mergington.edu", safe="")

    # Act
    response = client.delete(f"/activities/{unknown_activity}/participants/{encoded_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_participant_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missing@mergington.edu"
    encoded_activity = quote(activity_name, safe="")
    encoded_email = quote(missing_email, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants/{encoded_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
