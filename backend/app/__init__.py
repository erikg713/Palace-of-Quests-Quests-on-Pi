import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import config_by_name

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name: str = None) -> Flask:
    """
    Flask application factory. Initializes extensions, registers blueprints, error handlers, and logging.
    """
    app = Flask(__name__)

    # Load configuration
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", [
            "http://localhost:3000", "https://yourdomain.com"
        ])}}
    )
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

def register_blueprints(app: Flask) -> None:
    """
    Register all application blueprints.
    """
    # Blueprint imports
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

def register_error_handlers(app: Flask) -> None:
    """
    Register application-wide error handlers.
    """
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning("404 Not Found: %s", error)
        return jsonify(error="Resource not found"), 404

    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning("400 Bad Request: %s", error)
        return jsonify(error="Bad request"), 400

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error("500 Internal Server Error: %s", error)
        return jsonify(error="Internal server error"), 500

    @app.errorhandler(429)
    def ratelimit_handler(e):
        app.logger.warning("429 Rate Limit Exceeded: %s", e.description)
        return jsonify(error="Rate limit exceeded", message=str(e.description)), 429

def configure_jwt_handlers(app: Flask) -> None:
    """
    Configure JWT-related error handlers.
    """
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.info("JWT token expired.")
        return jsonify(error="Token has expired"), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        app.logger.info("JWT invalid token.")
        return jsonify(error="Invalid token"), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        app.logger.info("JWT missing token.")
        return jsonify(error="Authorization token required"), 401

def configure_logging(app: Flask) -> None:
    """
    Configure application logging using a rotating file handler.
    """
    log_dir = os.environ.get("LOG_DIR", "logs")
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "palace_of_quests.log"),
        maxBytes=10_240_000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    ))
    file_handler.setLevel(getattr(logging, log_level, logging.INFO))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, log_level, logging.INFO))
    if not app.debug and not app.testing:
        app.logger.info("Palace of Quests startup")
