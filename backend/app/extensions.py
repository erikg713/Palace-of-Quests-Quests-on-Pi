# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
cors = CORS()

def init_app(app):
    """
    Initialize all extensions with the Flask app instance.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    cors.init_app(app)
