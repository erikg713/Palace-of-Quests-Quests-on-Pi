def register_blueprints(app):
    """Register all application blueprints with optimal structure."""
    from app.blueprints.auth import auth_bp
    from app.blueprints.quests import quests_bp
    from app.blueprints.marketplace import marketplace_bp
    from app.blueprints.economy import economy_bp
    from app.blueprints.users import users_bp
    from app.blueprints.transactions import transactions_bp
    from app.blueprints.user_quests import user_quests_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.analytics import analytics_bp
    from app.blueprints.health import health_bp

    blueprints = [
        (auth_bp, '/api/auth'),
        (quests_bp, '/api/quests'),
        (marketplace_bp, '/api/marketplace'),
        (economy_bp, '/api/economy'),
        (users_bp, '/api/users'),
        (transactions_bp, '/api/transactions'),
        (user_quests_bp, '/api/user-quests'),
        (admin_bp, '/api/admin'),
        (analytics_bp, '/api/analytics'),
        (health_bp, '/api/health'),
    ]

    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import os

from config import config_by_name

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(key_func=get_remote_address)


def create_app(config_name=None):
    """Application factory pattern for creating Flask app instances."""
    
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=["http://localhost:3000", "https://yourdomain.com"])
    limiter.init_app(app)
    
    # Configure logging
    configure_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # JWT handlers
    configure_jwt_handlers(app)
    
    return app


def register_blueprints(app):
    """Register application blueprints."""
    
    from app.routes.auth import auth_bp
    from app.routes.quests import quests_bp
    from app.routes.marketplace import marketplace_bp
    from app.routes.economy import economy_bp
    from app.routes.users import users_bp
    from app.routes.admin import admin_bp
    from app.routes.analytics import analytics_bp
    
    blueprints = [
        (auth_bp, '/api/auth'),
        (quests_bp, '/api/quests'),
        (marketplace_bp, '/api/marketplace'),
        (economy_bp, '/api/economy'),
        (users_bp, '/api/users'),
        (admin_bp, '/api/admin'),
        (analytics_bp, '/api/analytics')
    ]
    
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def register_error_handlers(app):
    """Register application error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {'error': 'Rate limit exceeded', 'message': str(e.description)}, 429


def configure_jwt_handlers(app):
    """Configure JWT-related handlers."""
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization token required'}, 401


def configure_logging(app):
    """Configure application logging."""
    
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/palace_of_quests.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Palace of Quests startup')
