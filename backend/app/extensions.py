"""
Flask extension initializations and JWT configuration for Palace of Quests backend.

This module centralizes extension objects for import throughout the app.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO

from app.services.pi_network import PiNetworkService

# --- Extension Instances ---
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
pi_network = PiNetworkService()
websocket = SocketIO(cors_allowed_origins="*", async_mode="threading")

# --- JWT Error Handlers & Callbacks ---

# Consider moving error messages to a constants module if reused elsewhere.
_JWT_ERROR_RESPONSES = {
    "expired":   ({"message": "Token has expired", "error": "token_expired"}, 401),
    "invalid":   ({"message": "Invalid token", "error": "invalid_token"}, 401),
    "required":  ({"message": "Authentication token required", "error": "auth_required"}, 401),
}


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Checks if a JWT token's jti is blacklisted.
    Prevents usage of revoked tokens.
    """
    from app.models.auth import RevokedToken
    jti = jwt_payload.get('jti')
    if not jti:
        return True
    return RevokedToken.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handles expired JWT tokens."""
    return _JWT_ERROR_RESPONSES["expired"]


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handles invalid JWT tokens."""
    return _JWT_ERROR_RESPONSES["invalid"]


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handles missing JWT tokens."""
    return _JWT_ERROR_RESPONSES["required"]
"""
Flask Extensions Configuration
Centralized extension initialization for better dependency management.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_marshmallow import Marshmallow

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
cache = Cache()
ma = Marshmallow()

# Custom configurations
def configure_jwt(app):
    """Configure JWT settings and callbacks."""
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has expired', 'error': 'token_expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'message': 'Invalid token', 'error': 'invalid_token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'message': 'Authorization token required', 'error': 'authorization_required'}, 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has been revoked', 'error': 'token_revoked'}, 401
