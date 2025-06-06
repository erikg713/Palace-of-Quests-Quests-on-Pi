"""
Admin Blueprint: Quest Management, User Moderation
Author: Erik G. - Palace of Quests Team
Last Updated: 2025-06-06
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models import Quest, User, db
from app.utils.error_handlers import error_response

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return error_response("Admin privileges required.", 403)
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/quests', methods=['POST'])
@login_required
@admin_required
def create_quest():
    """Create a new quest (Admin only)"""
    data = request.get_json()
    title, description, reward, level_required = (
        data.get('title'), data.get('description'), data.get('reward'), data.get('level_required')
    )
    if not all([title, description, reward, level_required]):
        return error_response("All quest fields are required.", 400)
    quest = Quest(title=title, description=description, reward=reward, level_required=level_required)
    db.session.add(quest)
    db.session.commit()
    current_app.logger.info(f"Admin {current_user.username} created quest {title}")
    return jsonify({"success": True, "quest_id": quest.id}), 201

@admin_bp.route('/users/<int:user_id>/ban', methods=['POST'])
@login_required
@admin_required
def ban_user(user_id):
    """Ban a user (Admin only)"""
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    current_app.logger.warning(f"User {user.username} was banned by admin {current_user.username}")
    return jsonify({"success": True, "user_id": user_id, "status": "banned"})
