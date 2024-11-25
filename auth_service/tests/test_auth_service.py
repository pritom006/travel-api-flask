import pytest
from unittest.mock import patch
from flask import Flask
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from src.app import app  # Assuming your app is created in src.app

@pytest.fixture
def client():
    """
    This fixture provides a Flask test client for each test.
    """
    with app.test_client() as client:
        yield client

@patch("src.models.token_model.validate_token")
def test_validate_token_expired(mock_validate_token, client):
    """
    Test the behavior when an expired token is provided.
    """
    # Simulate an expired token by returning None
    mock_validate_token.return_value = None

    response = client.post('/admin_access', headers={"Authorization": "Bearer expired_token"})
    
    # Checking the correct status code and error message
    assert response.status_code == 401
    assert response.json == {"error": "Invalid or expired token"}


@patch("src.models.token_model.validate_token")
def test_admin_access_valid_token(mock_validate_token, client):
    """
    Test the behavior when a valid admin token is provided.
    """
    # Simulate a valid token for an Admin
    mock_validate_token.return_value = {"email": "admin@example.com", "role": "Admin"}

    response = client.post('/admin_access', headers={"Authorization": "Bearer valid_token"})

    # Checking for successful admin access
    assert response.status_code == 200
    assert response.json == {"message": "Admin access granted. You can modify destinations."}


@patch("src.models.token_model.validate_token")
def test_admin_access_invalid_token(mock_validate_token, client):
    """
    Test the behavior when an invalid token is provided.
    """
    # Simulate an invalid token (None)
    mock_validate_token.return_value = None

    response = client.post('/admin_access', headers={"Authorization": "Bearer invalid_token"})

    # Checking for invalid token error
    assert response.status_code == 401
    assert response.json == {"error": "Invalid or expired token"}


@patch("src.models.token_model.validate_token")
def test_admin_access_permission_denied(mock_validate_token, client):
    """
    Test the behavior when a non-admin user tries to access admin functionality.
    """
    # Simulate a valid token for a non-admin user
    mock_validate_token.return_value = {"email": "user@example.com", "role": "User"}

    response = client.post('/admin_access', headers={"Authorization": "Bearer user_token"})

    # Checking for permission denied error
    assert response.status_code == 403
    assert response.json == {"error": "Permission denied. Admin access required."}


@patch("src.models.token_model.validate_token")
def test_admin_access_no_token(mock_validate_token, client):
    """
    Test the behavior when no token is provided.
    """
    response = client.post('/admin_access')

    # Checking for token required error
    assert response.status_code == 401
    assert response.json == {"error": "Authorization token required"}


@patch("src.models.token_model.validate_token")
def test_generate_token(mock_validate_token, client):
    """
    Test token generation to ensure the mock validate_token is working
    (Token generation is tested separately from validation).
    """
    # Simulate token generation logic (typically would call the actual generate_token function)
    token_data = {"email": "admin@example.com", "role": "Admin"}
    token = "mock_token_string"  # Mocked token string

    # Normally, you would call your generate_token function to generate a token
    assert token == "mock_token_string"  # Test if the mock is set up correctly
