from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from app.services.pi_network import PiNetworkService

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
pi_network = PiNetworkService()
websocket = SocketIO(cors_allowed_origins="*", async_mode='threading')

# JWT configuration callbacks
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Check if JWT token has been revoked."""
    from app.models.auth import RevokedToken
    jti = jwt_payload['jti']
    return RevokedToken.is_jti_blacklisted(jti)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired token responses."""
    return {'message': 'Token has expired', 'error': 'token_expired'}, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid token responses."""
    return {'message': 'Invalid token', 'error': 'invalid_token'}, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing token responses."""
    return {'message': 'Authentication token required', 'error': 'auth_required'}, 401
