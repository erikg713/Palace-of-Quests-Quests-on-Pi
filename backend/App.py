from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://user:password@localhost/palace_of_quests')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import and register blueprints
from routes.auth import auth_bp
from routes.quests import quests_bp
from routes.marketplace import marketplace_bp
from routes.economy import economy_bp
from routes.users import users_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(quests_bp, url_prefix='/quests')
app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
app.register_blueprint(economy_bp, url_prefix='/economy')
app.register_blueprint(users_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)
