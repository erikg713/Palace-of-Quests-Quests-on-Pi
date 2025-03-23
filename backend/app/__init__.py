from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from app.middleware.error_handler import register_error_handlers

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name="development"):
    # Load environment variables
    load_dotenv()

    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)
    
    # Register error handlers
    register_error_handlers(app)

    # Load configuration
    config_class = {
        "production": "app.config.ProductionConfig",
        "testing": "app.config.TestingConfig",
        "development": "app.config.DevelopmentConfig"
    }.get(config_name, "app.config.DevelopmentConfig")
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    blueprints = [
        ("app.blueprints.auth", "auth_bp", "/auth"),
        ("app.blueprints.quests", "quests_bp", "/quests"),
        ("app.blueprints.marketplace", "marketplace_bp", "/marketplace"),
        ("app.blueprints.economy", "economy_bp", "/economy"),
        ("app.blueprints.users", "users_bp", "/users"),
        ("app.blueprints.transactions", "transactions_bp", "/transactions"),
        ("app.blueprints.user_quests", "user_quests_bp", "/user_quests"),
        ("app.blueprints.admin", "admin_bp", "/admin"),
        ("app.blueprints.analytics", "analytics_bp", "/analytics"),
        ("app.blueprints.health", "health_bp", "/health")
    ]
    
    for module, bp, url_prefix in blueprints:
        mod = __import__(module, fromlist=[bp])
        app.register_blueprint(getattr(mod, bp), url_prefix=url_prefix)

    return app
