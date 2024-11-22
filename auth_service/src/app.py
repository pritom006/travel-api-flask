from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from src.routes.auth_routes import auth_bp
import os

# Set up Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "../static"),
    static_url_path="/static"
)

# Enable CORS for all routes
CORS(app)

# Register Blueprint for auth routes
app.register_blueprint(auth_bp)

# Swagger UI configuration
SWAGGER_URL = '/swagger'  # URL to access Swagger UI
API_URL = '/static/swagger.json'  # Path to Swagger JSON

# Set up Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI URL
    API_URL,      # Swagger JSON file
    config={'app_name': "Auth Service API"}  # The app name displayed in Swagger UI
)

# Register Swagger UI Blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(port=5003, debug=True)
