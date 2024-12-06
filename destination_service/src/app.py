from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from src.routes.destination_routes import destination_bp
import os

# Set up Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "../static"),  
    static_url_path="/static" 
)

# Register Blueprint
app.register_blueprint(destination_bp)

# Swagger UI configuration
SWAGGER_URL = '/api/docs' 
API_URL = '/static/swagger.json'  

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,      
    config={'app_name': "Destination Service API"}
)

# Register Swagger UI Blueprint
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(port=5001, debug=True)


