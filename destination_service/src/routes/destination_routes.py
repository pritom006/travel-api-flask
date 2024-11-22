from flask import Blueprint
from src.controllers.destination_controller import get_destinations, delete_destination, add_new_destination

destination_bp = Blueprint('destinations', __name__)

# Route to get destinations based on the user's role
@destination_bp.route('/destinations', methods=['GET'])
def destinations():
    return get_destinations()

# Route to delete a destination (admin-only)
@destination_bp.route('/destinations/<int:destination_id>', methods=['DELETE'])
def delete(destination_id):
    return delete_destination(destination_id)

# Route to add a new destination (admin-only)
@destination_bp.route('/destinations', methods=['POST'])
def add_destination():
    return add_new_destination()
