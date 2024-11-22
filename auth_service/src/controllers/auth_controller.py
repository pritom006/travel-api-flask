from flask import jsonify, request
from pydantic import BaseModel, ValidationError
from src.models.token_model import validate_token

class AdminAccessRequest(BaseModel):
    token: str

def admin_access():
    """
    Validate the token and check for admin access.
    """
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Authorization token required"}), 401

    token = token.split(" ")[1]

    try:
        # Validate the structure of the token using Pydantic
        request_data = AdminAccessRequest(token=token)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    user_data = validate_token(request_data.token)

    if not user_data:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Check for Admin role
    if user_data['role'] != 'Admin':
        return jsonify({"error": "Permission denied. Admin access required."}), 403

    return jsonify({"message": "Admin access granted. You can modify destinations."}), 200
