from flask import request, jsonify
from functools import wraps
from .models import User
import jwt
import os

# Secret key for JWT (use a secure secret key in production)
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

# Middleware to verify JWT tokens
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Decode the JWT token
            token = token.split(" ")[1]  # Format: "Bearer <token>"
            decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_uid = decoded_data.get('uid')
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token', 'details': str(e)}), 401

        # Check if user exists in the database
        user = User.query.filter_by(uid=user_uid).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Add user to kwargs for access in the route
        kwargs['user'] = user
        return f(*args, **kwargs)
    return decorated

# Middleware to verify UID (used for Pi Network UIDs)
def uid_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        uid = request.headers.get('X-UID')  # Custom header for UID verification

        if not uid:
            return jsonify({'error': 'UID is missing'}), 401

        # Check if user exists in the database
        user = User.query.filter_by(uid=uid).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Add user to kwargs for access in the route
        kwargs['user'] = user
        return f(*args, **kwargs)
    return decorated
