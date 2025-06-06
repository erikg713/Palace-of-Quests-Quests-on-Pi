"""
Admin Blueprint: Quest Management, User Moderation
Author: Erik G. - Palace of Quests Team
Last Updated: 2025-06-06
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app.models import Quest, User, db
from app.utils.error_handlers import error_response
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    """Decorator to ensure the current user has admin privileges."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            current_app.logger.warning("Unauthorized admin access attempt by user: %s", getattr(current_user, 'username', 'Anonymous'))
            return error_response("Admin privileges required.", 403)
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/quests', methods=['POST'])
@login_required
@admin_required
def create_quest():
    """Create a new quest (Admin only)."""
    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid or missing JSON payload.", 400)

    required_fields = ("title", "description", "reward", "level_required")
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return error_response(f"Missing fields: {', '.join(missing_fields)}.", 400)

    try:
        quest = Quest(
            title=data['title'].strip(),
            description=data['description'].strip(),
            reward=data['reward'],
            level_required=data['level_required']
        )
        db.session.add(quest)
        db.session.commit()
        current_app.logger.info("Admin '%s' created quest '%s' (ID: %s)", current_user.username, quest.title, quest.id)
        return jsonify({"success": True, "quest_id": quest.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error("Quest creation failed: %s", str(e))
        return error_response("Failed to create quest. Please try again.", 500)

@admin_bp.route('/users/<int:user_id>/ban', methods=['POST'])
@login_required
@admin_required
def ban_user(user_id: int):
    """Ban a user (Admin only)."""
    user = User.query.get_or_404(user_id)
    if not user.is_active:
        return error_response("User is already banned.", 400)

    try:
        user.is_active = False
        db.session.commit()
        current_app.logger.warning("User '%s' (ID: %s) was banned by admin '%s'", user.username, user.id, current_user.username)
        return jsonify({"success": True, "user_id": user.id, "status": "banned"})
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error("Failed to ban user %s: %s", user.id, str(e))
        return error_response("Failed to ban user. Please try again.", 500)
