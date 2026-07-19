def test_get_activities_returns_expected_structure(client):
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert expected_keys.issubset(payload["Chess Club"].keys())


def test_get_activities_contains_known_seeded_activity(client):
    # Arrange
    activity_name = "Science Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert activity_name in payload
    assert isinstance(payload[activity_name]["participants"], list)
