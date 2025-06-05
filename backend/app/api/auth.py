"""Authentication Endpoints"""

import os
from flask import Blueprint, request
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import jwt

from app.models import db, User
from .utils import api_response, api_error

api_auth = Blueprint('api_auth', __name__)

@api_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    pi_wallet = data.get('pi_wallet')
    if not pi_wallet:
        return api_error("Missing required field: pi_wallet", 400)

    # Simulate Pi Network OAuth verification
    user = User.query.filter_by(pi_wallet=pi_wallet).first()
    if not user:
        return api_error("User not found", 404)

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY', 'defaultsecret'), algorithm='HS256')
    return api_response(data={'token': token, 'user': user.to_dict()}, message="Login successful")

@api_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    pi_wallet = data.get('pi_wallet')
    if not username or not pi_wallet:
        return api_error("Missing required fields: username and pi_wallet", 400)

    if User.query.filter((User.username == username) | (User.pi_wallet == pi_wallet)).first():
        return api_error("User with given username or pi_wallet already exists", 409)

    new_user = User(username=username, pi_wallet=pi_wallet, balance=0.0)
    db.session.add(new_user)
    db.session.commit()
    return api_response(data={'user_id': new_user.id}, message="User registered successfully", status_code=201)
