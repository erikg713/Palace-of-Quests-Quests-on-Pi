from flask import Blueprint, jsonify
from app.models import Achievement, UserAchievement, db

achievement_bp = Blueprint("achievement", __name__)

@achievement_bp.route("/get_achievements", methods=["GET"])
def get_achievements():
    achievements = Achievement.query.all()
    return jsonify([achievement.to_dict() for achievement in achievements])

@achievement_bp.route("/unlock_achievement/<int:achievement_id>", methods=["POST"])
def unlock_achievement(achievement_id):
    user_id = 1  # Replace with actual user retrieval
    user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement_id)
    db.session.add(user_achievement)
    db.session.commit()
    return jsonify({"message": "Achievement unlocked"})
