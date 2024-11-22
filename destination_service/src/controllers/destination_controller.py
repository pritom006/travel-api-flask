from flask import jsonify, request
from src.models.destination_model import destinations
from auth_service.src.models.token_model import validate_token
from pydantic import BaseModel

class DestinationRequest(BaseModel):
    name: str
    description: str
    location: str

class DeleteRequest(BaseModel):
    id: int

def get_destinations():
    """
    Returns all destinations, regardless of the user's role.
    """
    token = request.headers.get('Authorization')
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Authorization token required"}), 401

    token = token.split(" ")[1]
    user_data = validate_token(token)

    if not user_data:
        return jsonify({"error": "Invalid or expired token"}), 401

    # All users (regular users and admins) see all destinations
    return jsonify(list(destinations.values())), 200

def delete_destination(destination_id):
    """
    Deletes a destination by ID, admin-only functionality.
    """
    token = request.headers.get('Authorization')
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Authorization token required"}), 401

    token = token.split(" ")[1]
    user_data = validate_token(token)

    if not user_data:
        return jsonify({"error": "Invalid or expired token"}), 401

    if user_data.get("role") != "Admin":
        return jsonify({"error": "Permission denied. Admin access required."}), 403

    # Check if the destination exists
    if destination_id not in destinations:
        return jsonify({"error": "Destination not found"}), 404

    del destinations[destination_id]
    return jsonify({"message": "Destination deleted"}), 200

def add_new_destination():
    """
    Admin adds a new destination.
    """
    token = request.headers.get('Authorization')
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Authorization token required"}), 401

    token = token.split(" ")[1]
    user_data = validate_token(token)

    if not user_data:
        return jsonify({"error": "Invalid or expired token"}), 401

    if user_data.get("role") != "Admin":
        return jsonify({"error": "Permission denied. Admin access required."}), 403

    # Parse the request body
    try:
        destination_data = DestinationRequest(**request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Add the new destination
    new_id = max(destinations.keys()) + 1
    new_destination = {
        "id": new_id,
        "name": destination_data.name,
        "description": destination_data.description,
        "location": destination_data.location,
        "assigned_to": user_data.get("email")  # Optionally, can be assigned to the admin
    }

    destinations[new_id] = new_destination
    return jsonify({"message": "Destination added", "destination": new_destination}), 201
