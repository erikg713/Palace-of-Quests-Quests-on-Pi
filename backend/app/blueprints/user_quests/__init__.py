from flask import Blueprint

user_quests_bp = Blueprint('user_quests', __name__)

from . import routes

