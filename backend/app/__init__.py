from flask import Flask
from .models import db
from .routes import bp
from .subscription import subscription_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bp, url_prefix='/api')
    app.register_blueprint(subscription_bp, url_prefix='/api')

    return app
