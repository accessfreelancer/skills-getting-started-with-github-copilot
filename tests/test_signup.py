from urllib.parse import quote

from src import app as app_module


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert new_email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = app_module.activities[activity_name]["participants"][0]
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
