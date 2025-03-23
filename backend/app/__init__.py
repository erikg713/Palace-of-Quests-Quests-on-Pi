from flask import Flask
from app.models import db

def create_app(config_name="development"):
    app = Flask(__name__)
    
    # Load configuration
    if config_name == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif config_name == "testing":
        app.config.from_object("app.config.TestingConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")
    
    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
from flask_migrate import Migrate

migrate = Migrate()

def create_app(config_name="development"):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object("app.config.DevelopmentConfig")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    return app
from app.routes import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
from app.routes import quest as quest_blueprint
app.register_blueprint(quest_blueprint, url_prefix='/api')
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app(config_filename=None):
    # Load environment variables
    load_dotenv()

    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/palace_of_quests')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
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

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(quests_bp, url_prefix='/quests')
    app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
    app.register_blueprint(economy_bp, url_prefix='/economy')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(user_quests_bp, url_prefix='/user_quests')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(health_bp, url_prefix='/health')

    return app
