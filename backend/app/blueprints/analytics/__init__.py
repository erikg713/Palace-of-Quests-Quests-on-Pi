from flask import Blueprint

analytics_bp = Blueprint('analytics', __name__)

from . import routes

