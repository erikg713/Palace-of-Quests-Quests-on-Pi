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
