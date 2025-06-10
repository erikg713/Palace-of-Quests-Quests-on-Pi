from flask import Flask
from backend.extensions import db, migrate, cors
from backend.config import get_config
from backend.routes import register_blueprints
from dotenv import load_dotenv
import logging
import os

def create_app(config_name: str = None) -> Flask:
    """
    Flask application factory for Palace of Quests backend.
    """
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(get_config(config_name or os.getenv('FLASK_ENV', 'production')))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # Set up logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)

    app.logger.info(f"App started in {app.config['ENV']} mode.")

    return app

application = create_app()

if __name__ == "__main__":
    dev_app = create_app("development")
    dev_app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=dev_app.config.get('DEBUG', True)
    )
