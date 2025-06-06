"""
Admin Blueprint for Palace of Quests
Comprehensive administrative interface with proper access controls.
"""

from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

# Import views to register routes
from . import dashboard, users, quests, marketplace, transactions, analytics, system

__all__ = ['admin_bp']
