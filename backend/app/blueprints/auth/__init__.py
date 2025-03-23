# app/blueprints/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.blueprints.auth import routes, forms
