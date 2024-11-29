from flask import Blueprint, request, jsonify
import requests
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signin", methods=["POST"])
def signin():
    access_token = request.json.get("authResult")["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.minepi.com/v2/me", headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        # Process user_data as needed, e.g., create or update user in database
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not authorized"}), 401

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db
from app.utils.security import create_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        token = create_jwt({"user_id": user.id})
        response = jsonify({"message": "Logged in successfully"})
        response.set_cookie("access_token", token, httponly=True, secure=True)
        return response, 200
    return jsonify({"error": "Invalid credentials"}), 401
from flask import Blueprint, request, jsonify
import requests

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signin", methods=["POST"])
def signin():
    access_token = request.json.get("authResult")["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.minepi.com/v2/me", headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "User not authorized"}), 401

from flask import Blueprint, request, jsonify
import requests
import os

auth_bp = Blueprint("auth", __name__)
PI_API_BASE_URL = "https://api.minepi.com/v2"
PI_API_KEY = os.getenv("PI_API_KEY")

@auth_bp.route("/signin", methods=["POST"])
def signin():
    access_token = request.json.get("authResult")["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{PI_API_BASE_URL}/me", headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return jsonify({"error": "User verification failed"}), 401
    except Exception as err:
        print(f"Unexpected error: {err}")
        return jsonify({"error": "An unexpected error occurred"}), 500

from flask import Blueprint, request, jsonify
import requests

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signin", methods=["POST"])
def signin():
    access_token = request.json.get("authResult")["accessToken"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.minepi.com/v2/me", headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "User not authorized"}), 401
