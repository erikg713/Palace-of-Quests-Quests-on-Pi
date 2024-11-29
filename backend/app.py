from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from routes.auth import auth_bp
from routes.marketplace import marketplace_bp
from routes.quests import quests_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
app.register_blueprint(quests_bp, url_prefix='/quests')

if __name__ == '__main__':
    app.run(debug=True)

from dotenv import load_dotenv
import os

# Load the appropriate .env file
env_file = '.env.development' if os.getenv("FLASK_ENV") == 'development' else '.env.production'
load_dotenv(env_file)

# Access variables like this:
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
PI_API_KEY = os.getenv("PI_API_KEY")
