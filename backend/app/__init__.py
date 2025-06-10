"""
Palace of Quests Application Factory
Enhanced Flask application with modular architecture and security best practices.
"""

import os
import logging
from typing import Optional
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.extensions import db, migrate, jwt, bcrypt, cache
from app.core.auth import configure_auth_handlers
from app.core.errors import register_error_handlers
from app.core.logging import setup_logging
from app.middleware.security import SecurityMiddleware
from app.middleware.request_context import RequestContextMiddleware
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
from flask import Flask
from .config import get_config
from .extensions import db, migrate, cors
from .routes import register_blueprints
from .middleware import register_middlewares

def create_app(env=None):
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    register_middlewares(app)
    register_blueprints(app)

    return app

def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Application factory pattern for creating Flask instances.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = _get_config_class(config_name)
    app.config.from_object(config_class)
    
    # Setup logging first
    setup_logging(app)
    
    # Initialize extensions
    _initialize_extensions(app)
    
    # Configure middleware
    _configure_middleware(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    # Setup error handlers
    register_error_handlers(app)
    
    # Configure authentication
    configure_auth_handlers(app)
    
    # Setup rate limiting
    _setup_rate_limiting(app)
    
    app.logger.info(f"Application initialized in {app.config.get('ENV', 'unknown')} mode")
    
    return app


def _get_config_class(config_name: Optional[str]):
    """Get configuration class based on environment."""
    from app.config import config_map
    
    env = config_name or os.environ.get('FLASK_ENV', 'production').lower()
    return config_map.get(env, config_map['production'])


def _initialize_extensions(app: Flask) -> None:
    """Initialize Flask extensions with the app instance."""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    
    # CORS configuration for Pi Network integration
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "https://sandbox.minepi.com",
                "https://app.minepi.com",
                "http://localhost:3000"  # Development frontend
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })


def _configure_middleware(app: Flask) -> None:
    """Configure application middleware."""
    SecurityMiddleware(app)
    RequestContextMiddleware(app)


def _register_blueprints(app: Flask) -> None:
    """Register application blueprints with proper URL prefixes."""
    from app.blueprints.auth import auth_bp
    from app.blueprints.users import users_bp
    from app.blueprints.quests import quests_bp
    from app.blueprints.marketplace import marketplace_bp
    from app.blueprints.transactions import transactions_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.leaderboard import leaderboard_bp
    
    # API blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(quests_bp, url_prefix='/api/v1/quests')
    app.register_blueprint(marketplace_bp, url_prefix='/api/v1/marketplace')
    app.register_blueprint(transactions_bp, url_prefix='/api/v1/transactions')
    app.register_blueprint(leaderboard_bp, url_prefix='/api/v1/leaderboard')
    
    # Admin blueprint with separate prefix
    app.register_blueprint(admin_bp, url_prefix='/admin/api/v1')


def _setup_rate_limiting(app: Flask) -> None:
    """Configure rate limiting for API endpoints."""
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://')
    )
    
    # Store limiter in app for use in blueprints
    app.limiter = limiter
