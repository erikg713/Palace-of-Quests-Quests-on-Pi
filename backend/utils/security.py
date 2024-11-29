from flask import jsonify
import jwt
from functools import wraps
from datetime import datetime, timedelta
from app import app

def create_jwt(payload):
    payload['exp'] = datetime.utcnow() + timedelta(hours=1)  # Token expiration
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm="HS256")

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token:
            return jsonify({"error": "Authentication token is missing"}), 401
        try:
            jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated
