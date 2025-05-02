from flask import Flask
from flask_cors import CORS
from src.routes.base import register_base_routes
import src.config.config_handler as Config

from src.routes.gitlab import register_gitlab_routes
from src.routes.preferences import register_preferences_routes

app = Flask(__name__)

# Enable CORS for all endpoints
CORS(
    app,
    origins=Config.get_app_client_urls(),
    methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

# Register routes
register_base_routes(app)
register_preferences_routes(app)
register_gitlab_routes(app)

if __name__ == "__main__":
    app.run(
        debug=Config.get_app_debug(),
        host=Config.get_app_host(),
        port=Config.get_app_port(),
    )
