import pytest
from unittest.mock import patch, MagicMock
from flask import jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from src.app import app  # Assuming your app is created in src.app

# Mock data for destinations
mock_destinations = {
    1: {"id": 1, "name": "Paris", "description": "City of Light", "location": "France", "assigned_to": "user1"},
    2: {"id": 2, "name": "Tokyo", "description": "Land of the Rising Sun", "location": "Japan", "assigned_to": "user2"},
    3: {"id": 3, "name": "Dhaka", "description": "Land of Green", "location": "Bangladesh", "assigned_to": "admin"},
    4: {"id": 4, "name": "Kolkata", "description": "City of Joy", "location": "India", "assigned_to": "admin"},
    5: {"id": 5, "name": "Newyork", "description": "Land of the Golden Heart", "location": "USA", "assigned_to": "user3"},
}


@pytest.fixture
def client():
    """
    This fixture provides a Flask test client for each test.
    """
    with app.test_client() as client:
        yield client


# Test case for getting all destinations (should work for all users)
@patch("src.controllers.destination_controller.validate_token")
@patch("src.models.destination_model.destinations", new_callable=lambda: mock_destinations)
def test_get_destinations(mock_destinations, mock_validate_token, client):
    mock_validate_token.return_value = {"email": "user1@example.com", "role": "User"}
    response = client.get("/destinations", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    response_data = response.json
    assert len(response_data) == len(mock_destinations)
    assert any(dest["name"] == "Paris" for dest in response_data)


# Test case for adding a new destination (admin-only)
@patch("src.controllers.destination_controller.validate_token")
@patch("src.models.destination_model.destinations", new_callable=lambda: mock_destinations)
def test_add_new_destination(mock_destinations, mock_validate_token, client):
    mock_validate_token.return_value = {"email": "admin@example.com", "role": "Admin"}

    new_destination_data = {
        "name": "Berlin",
        "description": "Capital of Germany",
        "location": "Germany"
    }
    response = client.post("/destinations", json=new_destination_data, headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 201
    assert response.json["message"] == "Destination added"
    assert response.json["destination"]["name"] == "Berlin"
    assert len(mock_destinations) == 5


# Test case for deleting a destination (admin-only)
@patch("src.controllers.destination_controller.validate_token")
@patch("src.models.destination_model.destinations", new_callable=lambda: mock_destinations)
def test_delete_destination(mock_destinations, mock_validate_token, client):
    mock_validate_token.return_value = {"email": "admin@example.com", "role": "Admin"}

    destination_id_to_delete = 1
    response = client.delete(f"/destinations/{destination_id_to_delete}", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json["message"] == "Destination deleted"
    mock_destinations.pop(destination_id_to_delete, None)
    assert destination_id_to_delete not in mock_destinations


# Test case for non-admin user trying to delete a destination (should fail)
@patch("src.controllers.destination_controller.validate_token")
@patch("src.models.destination_model.destinations", new_callable=lambda: mock_destinations)
def test_delete_destination_permission_denied(mock_destinations, mock_validate_token, client):
    mock_validate_token.return_value = {"email": "user1@example.com", "role": "User"}

    destination_id_to_delete = 1
    response = client.delete(f"/destinations/{destination_id_to_delete}", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 403
    assert response.json["error"] == "Permission denied. Admin access required."


# Test case for invalid token
@patch("src.controllers.destination_controller.validate_token")
def test_get_destinations_invalid_token(mock_validate_token, client):
    mock_validate_token.return_value = None
    response = client.get("/destinations", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json["error"] == "Invalid or expired token"


# Test case for missing Authorization header
def test_missing_authorization_header(client):
    response = client.get("/destinations")
    assert response.status_code == 401
    assert response.json["error"] == "Authorization token required"


# Test for invalid role while adding a destination
@patch("src.controllers.destination_controller.validate_token")
def test_add_new_destination_invalid_role(mock_validate_token, client):
    mock_validate_token.return_value = {"email": "user1@example.com", "role": "User"}

    new_destination_data = {
        "name": "Berlin",
        "description": "Capital of Germany",
        "location": "Germany"
    }
    response = client.post("/destinations", json=new_destination_data, headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 403
    assert response.json["error"] == "Permission denied. Admin access required."


# Test for invalid destination data
@patch("src.controllers.destination_controller.validate_token")
def test_add_new_destination_invalid_data(mock_validate_token, client):
    mock_validate_token.return_value = {"email": "admin@example.com", "role": "Admin"}

    invalid_destination_data = {
        "name": ""  # Missing required fields
    }
    response = client.post("/destinations", json=invalid_destination_data, headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 400
    assert "error" in response.json


# Test for deleting a non-existing destination
@patch("src.controllers.destination_controller.validate_token")
def test_delete_non_existing_destination(mock_validate_token, client):
    mock_validate_token.return_value = {"email": "admin@example.com", "role": "Admin"}

    response = client.delete("/destinations/999", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 404
    assert response.json["error"] == "Destination not found"
