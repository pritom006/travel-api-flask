# In-memory storage for destinations
destinations = {
    1: {"id": 1, "name": "Paris", "description": "City of Light", "location": "France", "assigned_to": "user1"},
    2: {"id": 2, "name": "Tokyo", "description": "Land of the Rising Sun", "location": "Japan", "assigned_to": "user2"},
    3: {"id": 3, "name": "Dhaka", "description": "Land of Green", "location": "Bangladesh", "assigned_to": "admin"},
    4: {"id": 4, "name": "Kolkata", "description": "City of Joy", "location": "India", "assigned_to": "admin"},
    5: {"id": 5, "name": "Newyork", "description": "Land of the Golden Heart", "location": "USA", "assigned_to": "user3"},
}

def add_destination(destination):
    """ Add a new destination to the in-memory storage. """
    destinations[destination["id"]] = destination

