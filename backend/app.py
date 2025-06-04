"""
Palace of Quests Backend Application Factory

A production-ready Flask application with comprehensive configuration management,
middleware integration, and modular blueprint registration.
"""

import os
import logging
from typing import Optional, Dict, Any, List, Tuple
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Configuration constants
DEFAULT_CONFIG = {
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    },
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': False,
}

CORS_CONFIG = {
    'resources': {r"/*": {"origins": "*"}},
    'supports_credentials': True,
    'allow_headers': ['Content-Type', 'Authorization'],
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
}

BLUEPRINT_ROUTES = [
    ('auth', '/auth'),
    ('quests', '/quests'),
    ('marketplace', '/marketplace'),
    ('economy', '/economy'),
    ('users', '/users'),
    ('transactions', '/transactions'),
    ('user_quests', '/user_quests'),
    ('admin', '/admin'),
    ('analytics', '/analytics'),
    ('health', '/health'),
]


class ConfigurationError(Exception):
    """Raised when application configuration is invalid or missing."""
    pass


def validate_environment() -> None:
    """
    Validates required environment variables and configuration.
    
    Raises:
        ConfigurationError: If required configuration is missing or invalid.
    """
    required_vars = ['DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ConfigurationError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
    
    # Validate database URL format
    db_url = os.getenv('DATABASE_URL')
    if not any(db_url.startswith(prefix) for prefix in ['postgresql://', 'sqlite:///', 'mysql://']):
        raise ConfigurationError(
            f"Invalid DATABASE_URL format. Expected postgresql://, sqlite:///, or mysql:// prefix"
        )


def configure_database(app: Flask) -> None:
    """
    Configures database settings with production optimizations.
    
    Args:
        app: Flask application instance
    """
    db_url = os.getenv('DATABASE_URL')
    
    # Handle Heroku postgres URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    
    # Apply database configuration
    for key, value in DEFAULT_CONFIG.items():
        app.config.setdefault(key, value)


def initialize_extensions(app: Flask) -> None:
    """
    Initializes Flask extensions with the application context.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, **CORS_CONFIG)


def setup_middleware(app: Flask) -> None:
    """
    Configures application middleware with graceful error handling.
    
    Args:
        app: Flask application instance
    """
    middleware_modules = [
        ('middleware.logger', 'setup_logging', 'custom logging'),
        ('middleware.rate_limiter', 'init_rate_limiter', 'rate limiting'),
        ('middleware.error_handler', 'register_error_handlers', 'custom error handling'),
        ('middleware.security', 'init_security_headers', 'security headers'),
    ]
    
    for module_name, function_name, description in middleware_modules:
        try:
            module = __import__(module_name, fromlist=[function_name])
            middleware_func = getattr(module, function_name)
            middleware_func(app)
            app.logger.info(f"Initialized {description} middleware")
        except (ImportError, AttributeError) as e:
            app.logger.warning(
                f"Could not initialize {description} middleware: {str(e)}. "
                f"Continuing without {description}."
            )


def register_blueprints(app: Flask) -> None:
    """
    Registers application blueprints with error handling and logging.
    
    Args:
        app: Flask application instance
    """
    registered_routes = []
    failed_routes = []
    
    for route_name, url_prefix in BLUEPRINT_ROUTES:
        try:
            # Dynamic import of blueprint modules
            module = __import__(f'routes.{route_name}', fromlist=[f'{route_name}_bp'])
            blueprint = getattr(module, f'{route_name}_bp')
            
            app.register_blueprint(blueprint, url_prefix=url_prefix)
            registered_routes.append(f"{route_name} -> {url_prefix}")
            
        except (ImportError, AttributeError) as e:
            error_msg = f"Failed to register {route_name} blueprint: {str(e)}"
            app.logger.error(error_msg)
            failed_routes.append(route_name)
    
    # Log registration summary
    if registered_routes:
        app.logger.info(f"Registered blueprints: {', '.join(registered_routes)}")
    
    if failed_routes:
        app.logger.warning(f"Failed to register blueprints: {', '.join(failed_routes)}")


def import_models() -> None:
    """
    Imports application models for SQLAlchemy migration discovery.
    
    This ensures all models are available when running database migrations.
    """
    try:
        import models  # noqa: F401
        logging.info("Successfully imported application models")
    except ImportError as e:
        logging.warning(f"Could not import models module: {str(e)}")


def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Application factory for Palace of Quests backend.
    
    Creates and configures a Flask application instance with all necessary
    extensions, middleware, and blueprints.
    
    Args:
        config_name: Optional configuration name for different environments
        
    Returns:
        Configured Flask application instance
        
    Raises:
        ConfigurationError: If required configuration is missing or invalid
        RuntimeError: If application creation fails
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Validate configuration before proceeding
        validate_environment()
        
        # Create Flask application
        app = Flask(__name__)
        
        # Configure application
        configure_database(app)
        
        # Set environment-specific configuration
        if config_name:
            app.config['ENV'] = config_name
        
        # Initialize extensions
        initialize_extensions(app)
        
        # Setup middleware
        setup_middleware(app)
        
        # Import models for migrations
        import_models()
        
        # Register blueprints
        register_blueprints(app)
        
        # Log successful initialization
        app.logger.info(
            f"Palace of Quests application initialized successfully. "
            f"Environment: {app.config.get('ENV', 'production')}"
        )
        
        return app
        
    except ConfigurationError:
        raise
    except Exception as e:
        error_msg = f"Failed to create application: {str(e)}"
        logging.error(error_msg)
        raise RuntimeError(error_msg) from e


def create_development_app() -> Flask:
    """
    Creates a Flask application configured for development environment.
    
    Returns:
        Flask application with development settings
    """
    app = create_app('development')
    app.config.update({
        'DEBUG': True,
        'TESTING': False,
        'JSONIFY_PRETTYPRINT_REGULAR': True,
    })
    return app


def create_production_app() -> Flask:
    """
    Creates a Flask application configured for production environment.
    
    Returns:
        Flask application with production settings
    """
    app = create_app('production')
    app.config.update({
        'DEBUG': False,
        'TESTING': False,
        'SESSION_COOKIE_SECURE': True,
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_SAMESITE': 'Lax',
    })
    return app


# Application instance for WSGI servers
application = create_app()

if __name__ == '__main__':
    # Development server
    dev_app = create_development_app()
    dev_app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=True
        )
