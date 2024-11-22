from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from src.routes.destination_routes import destination_bp
import os

# Set up Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "../static"),  # Correct static folder
    static_url_path="/static"  # URL path for accessing static files
)

# Register Blueprint
app.register_blueprint(destination_bp)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # URL to access Swagger UI
API_URL = '/static/swagger.json'  # Path to Swagger JSON

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI URL
    API_URL,      # Swagger JSON file
    config={'app_name': "Destination Service API"}
)

# Register Swagger UI Blueprint
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(port=5001, debug=True)


