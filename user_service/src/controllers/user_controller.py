from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user_model import users
from src.utils.jwt_utils import create_access_token
from pydantic import BaseModel, EmailStr, ValidationError

# Pydantic models for validation
class RegisterModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

def register_user():
    data = request.json

    try:
        validated_data = RegisterModel(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if validated_data.email in [u["email"] for u in users]:
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(validated_data.password)
    user = {
        "name": validated_data.name,
        "email": validated_data.email,
        "password": hashed_password,
        "role": validated_data.role,
    }
    users.append(user)

    return jsonify({"message": "User registered successfully"}), 201


def login_user():
    data = request.json

    try:
        validated_data = LoginModel(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    user = next((u for u in users if u["email"] == validated_data.email), None)

    if user and check_password_hash(user["password"], validated_data.password):
        token = create_access_token(user["email"], user["role"])
        return jsonify({"message": "Login successful", "access_token": token}), 200

    return jsonify({"error": "Invalid email or password"}), 401


def get_user_profile(email):
    user = next((u for u in users if u["email"] == email), None)
    if user:
        return jsonify({"name": user["name"], "email": user["email"], "role": user["role"]}), 200
    return jsonify({"error": "User not found"}), 404
