from flask import Blueprint, request, jsonify
from src.controllers.user_controller import register_user, login_user, get_user_profile
from src.utils.jwt_utils import token_required

# Create a blueprint for user routes
user_bp = Blueprint('user', __name__)

# Register endpoint
@user_bp.route('/register', methods=['POST'])
def register():
    return register_user()

# Login endpoint
@user_bp.route('/login', methods=['POST'])
def login():
    return login_user()

# Profile endpoint (protected)
@user_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return get_user_profile(current_user["email"])
