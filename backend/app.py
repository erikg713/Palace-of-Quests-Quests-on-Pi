from flask import Flask
from backend.extensions import db, migrate, cors
from backend.config import get_config
from backend.routes import register_blueprints
from dotenv import load_dotenv
import logging
import os
from flask import Flask, request, jsonify
import requests
import jwt  # Install with `pip install pyjwt`
import os

app = Flask(__name__)
PI_AUTH_URL = "https://api.minepi.com/v2"
PI_API_KEY = os.getenv("PI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route("/auth", methods=["POST"])
def authenticate():
    data = request.json
    user_token = data.get("access_token")
    
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(f"{PI_AUTH_URL}/me", headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        token = jwt.encode(user_data, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token, "user": user_data}), 200
    else:
        return jsonify({"error": "Authentication failed"}), 401

if __name__ == "__main__":
    app.run(debug=True)
def create_app(config_name: str = None) -> Flask:
    """
    Flask application factory for Palace of Quests backend.
    """
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(get_config(config_name or os.getenv('FLASK_ENV', 'production')))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # Set up logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)

    app.logger.info(f"App started in {app.config['ENV']} mode.")

    return app

application = create_app()

if __name__ == "__main__":
    dev_app = create_app("development")
    dev_app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=dev_app.config.get('DEBUG', True)
    )

# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Pi Network Authentication
PI_AUTH_URL = "https://api.minepi.com/v2"
PI_API_KEY = os.getenv("PI_API_KEY")

@app.route("/auth", methods=["POST"])
def authenticate():
    data = request.json
    user_token = data.get("access_token")
    
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(f"{PI_AUTH_URL}/me", headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Authentication failed"}), 401

if __name__ == "__main__":
    app.run(debug=True)
