import os
import jwt
from functools import wraps
from flask import request, jsonify
from models import User

def requires_role(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]
            if not token:
                return jsonify({'error': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, os.getenv('SECRET_KEY', 'defaultsecret'), algorithms=['HS256'])
                user_id = data.get('user_id')
                user = User.query.get(user_id)
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                if user.role != role:
                    return jsonify({'error': 'Insufficient privileges'}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except Exception as e:
                return jsonify({'error': f'Invalid token: {str(e)}'}), 401

            return f(*args, **kwargs)
        return decorated
    return decorator
