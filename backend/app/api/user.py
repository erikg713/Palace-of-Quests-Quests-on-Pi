"""User Profile Endpoints"""

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from .utils import api_response, api_error

api_user = Blueprint('api_user', __name__)

@api_user.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user = User.query.get(get_jwt_identity())
    if not user:
        return api_error("User not found", 404)
    return api_response(data=user.to_dict())
