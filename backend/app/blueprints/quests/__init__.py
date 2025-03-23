from flask import Blueprint

quests_bp = Blueprint('quests', __name__)

from . import routes

