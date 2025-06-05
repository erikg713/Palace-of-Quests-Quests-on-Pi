"""
This package contains all the route modules for the backend application.
The __init__.py file is used to organize and initialize these routes for use in the Flask app.
"""from flask import Flask

def init_app(app: Flask):
    from .user_routes import user_blueprint
    from .admin_routes import admin_blueprint
    
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)from .user_routes import user_blueprint
from .admin_routes import admin_blueprint

__all__ = ["user_blueprint", "admin_blueprint"]
