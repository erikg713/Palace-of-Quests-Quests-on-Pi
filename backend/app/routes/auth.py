from flask import Blueprint, request, jsonify
import os
import jwt
from datetime import datetime, timedelta
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    pi_wallet = data.get('pi_wallet')

    if not username or not pi_wallet:
        return jsonify({'error': 'Missing required fields: username and pi_wallet'}), 400

    # Check if user already exists
    existing_user = User.query.filter((User.username == username) | (User.pi_wallet == pi_wallet)).first()
    if existing_user:
        return jsonify({'error': 'User with given username or pi_wallet already exists'}), 400

    new_user = User(username=username, pi_wallet=pi_wallet, balance=0.0)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    pi_wallet = data.get('pi_wallet')
    
    if not pi_wallet:
        return jsonify({'error': 'Missing required field: pi_wallet'}), 400
    
    # Simulate Pi Network OAuth verification process
    # In production, you would verify the Pi Network token here
    user = User.query.filter_by(pi_wallet=pi_wallet).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Generate JWT token for session management
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY', 'defaultsecret'), algorithm='HS256')
    
    return jsonify({'message': 'Login successful', 'token': token}), 200
