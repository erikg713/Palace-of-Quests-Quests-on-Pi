import os
import base64
import hashlib
import hmac
import json
from flask import Flask, request, jsonify, session, g
from functools import wraps
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.quests import quests_bp
    from app.blueprints.marketplace import marketplace_bp
    from app.blueprints.transactions import transactions_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(quests_bp, url_prefix='/api/quests')
    app.register_blueprint(marketplace_bp, url_prefix='/api/marketplace')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')

    return app
def verify_pi_auth(payload: dict, signature: str, pi_api_key: str) -> bool:
    """
    Verifies the Pi Network authentication payload using HMAC SHA256.
    Follows Pi Network's backend verification guide.
    """
    message = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    signature_bytes = base64.b64decode(signature)
    expected_signature = hmac.new(
        key=pi_api_key.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return hmac.compare_digest(signature_bytes, expected_signature)

def pi_login_required(fn):
    """
    Decorator to protect routes, requiring Pi authentication.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = session.get('pi_user')
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        g.pi_user = user
        return fn(*args, **kwargs)
    return wrapper

def configure_pi_auth_handlers(app: Flask):
    # Set your Pi API key as an environment variable for security
    app.config['PI_API_KEY'] = os.environ.get('PI_API_KEY', 'replace_with_real_key')

    @app.route('/pi/auth', methods=['POST'])
    def pi_auth():
        """
        Frontend sends: { payload: {...}, signature: "..." }
        """
        data = request.get_json()
        payload = data.get('payload')
        signature = data.get('signature')
        api_key = app.config['PI_API_KEY']
        if not payload or not signature:
            return jsonify({'error': 'Invalid request'}), 400

        if not verify_pi_auth(payload, signature, api_key):
            return jsonify({'error': 'Invalid signature'}), 401

        # Optionally: check user fields, save in session
        session['pi_user'] = {
            'username': payload.get('username'),
            'uid': payload.get('uid'),
            # Add any fields you want to use for the session
        }
        return jsonify({'msg': 'Authentication successful', 'user': session['pi_user']})

    @app.route('/logout', methods=['POST'])
    def logout():
        session.pop('pi_user', None)
        return jsonify({'msg': 'Logged out'})

    # Example protected endpoint
    @app.route('/protected', methods=['GET'])
    @pi_login_required
    def protected():
        user = g.pi_user
        return jsonify({'msg': f'Hello, {user["username"]}! This is a protected route.'})

def create_app():
    app = Flask(__name__)
    # Use a strong secret key in production!
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'replace_with_a_real_secret')
    configure_pi_auth_handlers(app)
    return app
