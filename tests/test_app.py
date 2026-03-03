from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_root_redirects_to_static():
    # Arrange (client already created)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    # Arrange
    expected = activities.copy()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # ensure fresh copy
    activities[activity]["participants"] = []

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data.get("message", "")
    assert email in activities[activity]["participants"]


def test_signup_not_found():
    # Arrange
    organization = "NonExistent"

    # Act
    response = client.post(f"/activities/{organization}/signup", params={"email": "foo@bar"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
