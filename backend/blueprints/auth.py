from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from utils.jwt import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if AuthService.user_exists(username):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    AuthService.create_user(username, hashed_password)
    
    return jsonify({"message": "User registered successfully"}), 201

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = AuthService.get_user(username)

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200
