import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://user:password@localhost/palace_of_quests')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up logging middleware
from middleware.logger import setup_logging
setup_logging(app)

# Set up rate limiter
from middleware.rate_limiter import init_rate_limiter
init_rate_limiter(app)

# Ensure required dependencies are installed
try:
    import psycopg2
except ImportError:
    raise ImportError("psycopg2 is not installed. Please install it using 'pip install psycopg2-binary'")

# Import models
from models import User, Quest, Item, Transaction, UserQuest

# Import and register blueprints
from routes.auth import auth_bp
from routes.quests import quests_bp
from routes.marketplace import marketplace_bp
from routes.economy import economy_bp
from routes.users import users_bp
from routes.transactions import transactions_bp
from routes.user_quests import user_quests_bp
from routes.admin import admin_bp
from routes.analytics import analytics_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(quests_bp, url_prefix='/quests')
app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
app.register_blueprint(economy_bp, url_prefix='/economy')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(transactions_bp, url_prefix='/transactions')
app.register_blueprint(user_quests_bp, url_prefix='/user_quests')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(analytics_bp, url_prefix='/analytics')

if __name__ == '__main__':
    app.run(debug=True)


