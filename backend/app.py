from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import and register routes
from routes.auth import auth_bp
from routes.level import level_bp
from routes.shop import shop_bp
from routes.subscription import subscription_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(level_bp, url_prefix="/levels")
app.register_blueprint(shop_bp, url_prefix="/shop")
app.register_blueprint(subscription_bp, url_prefix="/subscription")

if __name__ == "__main__":
    app.run(debug=True)
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from config import Config
from routes.auth import auth_bp
from routes.marketplace import marketplace_bp
from routes.quests import quests_bp

# Load environment variables
env_file = '.env.development' if os.getenv("FLASK_ENV") == 'development' else '.env.production'
load_dotenv(env_file)

# Access environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
PI_API_KEY = os.getenv("PI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
app.register_blueprint(quests_bp, url_prefix='/quests')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)