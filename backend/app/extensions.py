"""
Centralized initialization and configuration of Flask extensions for Palace of Quests backend.
Ensures all extensions are imported from a single source for maintainability.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow

from app.services.pi_network import PiNetworkService

# --- Extension Instances ---
db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
jwt: JWTManager = JWTManager()
bcrypt: Bcrypt = Bcrypt()
cache: Cache = Cache()
limiter: Limiter = Limiter(key_func=get_remote_address)
websocket: SocketIO = SocketIO(cors_allowed_origins="*", async_mode="threading")
ma: Marshmallow = Marshmallow()
pi_network: PiNetworkService = PiNetworkService()

# --- JWT Error Response Utility ---
def _jwt_error_response(message: str, error_code: str, status_code: int = 401):
    """Utility for consistent JWT error responses."""
    return {"message": message, "error": error_code}, status_code

# --- JWT Configuration ---
def configure_jwt(app):
    """
    Attach JWT error handlers and revoke logic.
    Should be called in your app factory after initializing extensions.
    """
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload) -> bool:
        """Check if a JWT's jti is blacklisted."""
        from app.models.auth import RevokedToken
        jti = jwt_payload.get("jti")
        return not jti or RevokedToken.is_jti_blacklisted(jti)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return _jwt_error_response("Token has expired", "token_expired")

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return _jwt_error_response("Invalid token", "invalid_token")

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return _jwt_error_response("Authentication token required", "auth_required")

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return _jwt_error_response("Token has been revoked", "token_revoked")

# Usage (in your app factory):
# from .extensions import db, migrate, jwt, configure_jwt, ...
# db.init_app(app)
# migrate.init_app(app, db)
# jwt.init_app(app)
# configure_jwt(app)
# ...
