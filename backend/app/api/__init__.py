"""API Blueprint Registration for Palace of Quests"""

from flask import Blueprint
from .auth import api_auth
from .quests import api_quests
from .payments import api_payments
from .user import api_user

api = Blueprint('api', __name__)

# Register all API sub-blueprints
api.register_blueprint(api_auth, url_prefix='/auth')
api.register_blueprint(api_quests, url_prefix='/quests')
api.register_blueprint(api_payments, url_prefix='/payments')
api.register_blueprint(api_user, url_prefix='/user')
