from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.security import create_jwt, jwt_required
from app.models import User, db

auth_bp = Blueprint('auth', __name__)

# Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409

    # Hash the password and save the user
    hashed_password = generate_password_hash(data['password'])
    user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# User login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    # Find the user
    user = User.query.filter_by(username=data['username']).first()

    # Check credentials
    if user and check_password_hash(user.password_hash, data['password']):
        token = create_jwt({"user_id": user.id})
        response = make_response(jsonify({"message": "Logged in successfully"}))
        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=True,  # Use secure cookies in production
            samesite='Strict'  # Prevent CSRF
        )
        return response, 200

    return jsonify({"error": "Invalid credentials"}), 401