# backend/app/blueprints/analytics/__init__.py

from flask import Blueprint

analytics_bp = Blueprint("analytics", __name__)

# Import routes to register endpoints with the blueprint
from . import routes  # noqa: E402, F401
