from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        from .routes import auth, payments, game
        app.register_blueprint(auth.auth_bp, url_prefix='/auth')
        app.register_blueprint(payments.payments_bp, url_prefix='/payments')
        app.register_blueprint(game.game_bp, url_prefix='/game')
        db.create_all()

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        from .routes import auth, payments
        app.register_blueprint(auth.auth_bp, url_prefix='/auth')
        app.register_blueprint(payments.payments_bp, url_prefix='/payments')
        db.create_all()

    return app

# backend/app/__init__.py
from .routes import premium
app.register_blueprint(premium.premium_bp, url_prefix='/premium')
