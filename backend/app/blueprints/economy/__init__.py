from flask import Blueprint

economy_bp = Blueprint('economy', __name__)

from . import routes

