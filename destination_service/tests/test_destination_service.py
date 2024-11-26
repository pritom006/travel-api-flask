import pytest
from unittest.mock import patch
from flask import jsonify
from src.app import app

# Mock data for destinations
mock_destinations = {
    1: {"id": 1, "name": "Paris", "description": "City of Light", "location": "France", "assigned_to": "user1"},
    2: {"id": 2, "name": "Tokyo", "description": "Land of the Rising Sun", "location": "Japan", "assigned_to": "user2"},
    3: {"id": 3, "name": "Dhaka", "description": "Land of Green", "location": "Bangladesh", "assigned_to": "admin"},
    4: {"id": 4, "name": "Kolkata", "description": "City of Joy", "location": "India", "assigned_to": "admin"},
    5: {"id": 5, "name": "New York", "description": "Land of the Golden Heart", "location": "USA", "assigned_to": "user3"},
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
@patch("src.models.destination_model.destinations", mock_destinations)
def test_get_destinations(mock_validate_token, client):
    mock_validate_token.return_value = {"email": "user1@example.com", "role": "User"}
    assert len(mock_destinations) == 5
    response = client.get("/destinations", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200  
    response_data = response.json
    assert len(response_data) == len(mock_destinations)
    
    # Additional assertions to verify the content of the response
    assert any(dest["name"] == "Paris" for dest in response_data)
    assert any(dest["name"] == "Tokyo" for dest in response_data)
    assert any(dest["name"] == "Dhaka" for dest in response_data)
    assert any(dest["name"] == "Kolkata" for dest in response_data)
    assert any(dest["name"] == "Newyork" for dest in response_data)
    print(response_data)
    
    


# Test case for adding a new destination (admin-only)
@patch("src.controllers.destination_controller.validate_token")
@patch("src.models.destination_model.destinations", mock_destinations)
def test_add_new_destination(mock_validate_token, mock_destinations, client):
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
    assert len(mock_destinations) == 6
    assert any(dest["name"] == "Berlin" for dest in mock_destinations.values())


# Test case for deleting a destination (admin-only)
@patch("src.controllers.destination_controller.validate_token")
@patch("src.models.destination_model.destinations", mock_destinations)
def test_delete_destination(mock_validate_token, mock_destinations, client):
    mock_validate_token.return_value = {"email": "admin@example.com", "role": "Admin"}
    
    destination_id_to_delete = 1
    response = client.delete(f"/destinations/{destination_id_to_delete}", headers={"Authorization": "Bearer valid_token"})
    
    assert response.status_code == 200
  
    assert response.json["message"] == "Destination deleted"
    assert destination_id_to_delete not in mock_destinations


# Test case for non-admin user trying to delete a destination (should fail)
@patch("src.controllers.destination_controller.validate_token")
@patch("src.models.destination_model.destinations", mock_destinations)
def test_delete_destination_permission_denied(mock_validate_token, mock_destinations, client):
    mock_validate_token.return_value = {"email": "user1@example.com", "role": "User"}
    
    destination_id_to_delete = 1
    response = client.delete(f"/destinations/{destination_id_to_delete}", headers={"Authorization": "Bearer valid_token"})
    
    assert response.status_code == 403
    assert response.json["error"] == "Permission denied. Admin access required."


# Test case for invalid token
@patch("src.controllers.destination_controller.validate_token")
@patch("src.models.destination_model.destinations", mock_destinations)
def test_get_destinations_invalid_token(mock_validate_token, mock_destinations, client):
    mock_validate_token.return_value = None
    
    response = client.get("/destinations", headers={"Authorization": "Bearer invalid_token"})
    
    assert response.status_code == 401
    
    assert response.json["error"] == "Invalid or expired token"
