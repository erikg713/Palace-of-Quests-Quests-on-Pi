"""
Blueprints package initializer.

Exposes all application blueprints for easy import and registration.
Each blueprint encapsulates a distinct feature or logical area of the app.
"""

from .admin import admin_bp
from .analytics import analytics_bp
from .auth import auth_bp
from .economy import economy_bp
from .health import health_bp
from .marketplace import marketplace_bp
from .quests import quests_bp
from .transactions import transactions_bp
from .user_quests import user_quests_bp
from .users import users_bp

# List of all blueprints for bulk registration if needed
# Usage example in your app factory:
#   from app.blueprints import all_blueprints
#   for bp in all_blueprints:
#       app.register_blueprint(bp)
all_blueprints = [
    admin_bp,
    analytics_bp,
    auth_bp,
    economy_bp,
    health_bp,
    marketplace_bp,
    quests_bp,
    transactions_bp,
    user_quests_bp,
    users_bp,
]

__all__ = [
    "admin_bp",
    "analytics_bp",
    "auth_bp",
    "economy_bp",
    "health_bp",
    "marketplace_bp",
    "quests_bp",
    "transactions_bp",
    "user_quests_bp",
    "users_bp",
    "all_blueprints",
]
from .auth import auth_bp
from .quests import quests_bp
from .marketplace import marketplace_bp
from .economy import economy_bp
from .users import users_bp
from .transactions import transactions_bp
from .user_quests import user_quests_bp
from .admin import admin_bp
from .analytics import analytics_bp
from .health import health_bp
