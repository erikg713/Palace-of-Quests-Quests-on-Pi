from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.user import User, db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    hashed_password = generate_password_hash(data["password"])
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password_hash, data["password"]):
        token = create_access_token(identity={"id": user.id, "username": user.username})
        return jsonify({"access_token": token}), 200

    return jsonify({"message": "Invalid credentials"}), 401
# Authentication routes
from flask import Blueprint, request, jsonify
from models import User
from utils.security import hash_password, verify_password, create_jwt_token
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = hash_password(data['password'])
    user = User(username=data['username'], password_hash=hashed_password, wallet_address=data['wallet_address'])
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and verify_password(data['password'], user.password_hash):
        token = create_jwt_token(user.id)
        return jsonify(access_token=token), 200
    return jsonify(message="Invalid credentials"), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(username=user.username, wallet_address=user.wallet_address), 200
