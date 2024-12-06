import pytest
from unittest.mock import patch
from flask import Flask
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from src.app import app

@pytest.fixture
def client():
    """
    This fixture provides a Flask test client for each test.
    """
    with app.test_client() as client:
        yield client


@patch("src.models.user_model.users", [])
def test_register_user(client):
    """
    Test the behavior of user registration.
    """
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
        "role": "User"
    }

    response = client.post("/register", json=user_data)
    
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}


@patch("src.models.user_model.users", [])
def test_register_user_email_exists(client):
    """
    Test the behavior when attempting to register with an existing email.
    """
    existing_user = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "password": "securepassword",
        "role": "User"
    }

    # Simulate that the user already exists in the database
    mock_users = [existing_user]

    # Send a request to register with the same email
    user_data = {
        "name": "John Doe",
        "email": "jane.doe@example.com",  # Same email as the existing user
        "password": "newpassword",
        "role": "User"
    }

    with patch("src.models.user_model.users", mock_users):
        response = client.post("/register", json=user_data)
    
    assert response.status_code == 400
    assert response.json == {"error": "Email already exists"}


@patch("src.models.user_model.users", [
    {"name": "Admin", "email": "admin@example.com", "password": "hashedpassword", "role": "Admin"}
])
@patch("src.utils.jwt_utils.create_access_token")
def test_login_user_valid(mock_create_token, mock_users, client):
    """
    Test the behavior when a valid login is provided.
    """
    login_data = {
        "email": "admin@example.com",
        "password": "hashedpassword"
    }

    mock_create_token.return_value = "mocked_token_string"
    
    # Mock password hash checking
    with patch("werkzeug.security.check_password_hash") as mock_check_password:
        mock_check_password.return_value = True
        response = client.post("/login", json=login_data)
    
    assert response.status_code == 200
    assert response.json["message"] == "Login successful"
    assert "access_token" in response.json


@patch("src.models.user_model.users", [
    {"name": "Admin", "email": "admin@example.com", "password": "hashedpassword", "role": "Admin"}
])
def test_login_user_invalid_password(client):
    """
    Test the behavior when an invalid password is provided during login.
    """
    login_data = {
        "email": "admin@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/login", json=login_data)
    
    assert response.status_code == 401
    assert response.json == {"error": "Invalid email or password"}


@patch("src.models.user_model.users", [
    {"name": "Admin", "email": "admin@example.com", "password": "hashedpassword", "role": "Admin"}
])
@patch("src.utils.jwt_utils.token_required")
def test_get_user_profile(mock_token_required, client):
    """
    Test the behavior of fetching user profile (protected endpoint).
    """
    mock_token_required.return_value = {
        "email": "admin@example.com",
        "role": "Admin"
    }

    response = client.get("/profile", headers={"Authorization": "Bearer valid_token"})

    assert response.status_code == 200
    assert response.json["name"] == "Admin"
    assert response.json["email"] == "admin@example.com"
    assert response.json["role"] == "Admin"


@patch("src.models.user_model.users", [])
def test_get_user_profile_user_not_found(client):
    """
    Test the behavior when fetching a user profile for a non-existent user.
    """
    response = client.get("/profile", headers={"Authorization": "Bearer invalid_token"})
    
    assert response.status_code == 401
    assert response.json == {"error": "User not found"}
