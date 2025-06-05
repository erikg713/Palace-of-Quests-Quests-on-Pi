from flask import Blueprint, request, jsonify
import os
import jwt
from datetime import datetime, timedelta
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    username = data.get('username', '').strip()
    pi_wallet = data.get('pi_wallet', '').strip()

    if not username or not pi_wallet:
        return jsonify({'error': 'Missing required fields: username and pi_wallet'}), 400

    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == username) | (User.pi_wallet == pi_wallet)
    ).first()
    if existing_user:
        return jsonify({'error': 'User with given username or pi_wallet already exists'}), 409

    new_user = User(username=username, pi_wallet=pi_wallet, balance=0.0)
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

    return jsonify({
        'message': 'User registered successfully',
        'user_id': new_user.id
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    pi_wallet = data.get('pi_wallet', '').strip()
    if not pi_wallet:
        return jsonify({'error': 'Missing required field: pi_wallet'}), 400

    user = User.query.filter_by(pi_wallet=pi_wallet).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        # Log a warning in real usage, don't expose in prod
        secret_key = 'defaultsecret'

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return jsonify({
        'message': 'Login successful',
        'token': token
    }), 200
