"""
This package contains all the route modules for the backend application.
The __init__.py file is used to organize and initialize these routes for use in the Flask app.
"""

from flask import Flask
from .auth import auth_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    # Register other blueprints here

def init_app(app: Flask):
    """
    Initialize and register all blueprints for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    from .user_routes import user_blueprint
    from .admin_routes import admin_blueprint

    # Registering blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)

# Explicitly define what is accessible when using `from routes import *`
__all__ = []  # No global exports from this module
