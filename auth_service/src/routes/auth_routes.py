from flask import Blueprint
from src.controllers.auth_controller import admin_access

auth_bp = Blueprint('auth', __name__)

# Endpoint to check Admin access for destination management
@auth_bp.route('/admin_access', methods=['POST'])
def check_admin_access():
    return admin_access()
