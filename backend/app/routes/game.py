from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Level, db

bp = Blueprint("game", __name__, url_prefix="/game")

@bp.route("/progress", methods=["POST"])
@jwt_required()
def progress():
    user_id = get_jwt_identity()
    data = request.json

    user = User.query.get(user_id)
    new_level = data.get("level", user.level)

    if new_level > user.level:
        user.level = new_level
        user.experience_points += data.get("experience", 0)
        db.session.commit()

    return jsonify({"message": "Progress updated", "level": user.level}), 200
from flask import Blueprint, request, jsonify, g
from app.models import Quest, UserQuest, db

game_bp = Blueprint("game", __name__)

@game_bp.route("/quests", methods=["GET"])
def get_quests():
    # Assuming quests are user-specific, or we can fetch all quests
    quests = Quest.query.all()  # Modify to filter based on the user if needed
    return jsonify([quest.to_dict() for quest in quests])

@game_bp.route("/complete_quest/<int:quest_id>", methods=["POST"])
def complete_quest(quest_id):
    # Get current user dynamically from the authentication context
    user = g.user  # Assuming `g.user` holds the current user object after authentication

    # Get the quest from the database
    quest = Quest.query.get(quest_id)
    
    if not quest:
        return jsonify({"error": "Quest not found"}), 404
    
    # Check if the user has already completed this quest (to prevent duplicates)
    user_quest = UserQuest.query.filter_by(user_id=user.id, quest_id=quest.id).first()
    if user_quest and user_quest.is_completed:
        return jsonify({"message": "Quest already completed"}), 400

    # Update quest completion status
    quest.is_completed = True
    user_quest = UserQuest(user_id=user.id, quest_id=quest.id, is_completed=True)
    db.session.add(user_quest)

    # Optionally, award rewards for completing the quest (e.g., items, experience points)
    user.currency += quest.reward_currency  # Assuming a `reward_currency` field on the quest model
    user.experience_points += quest.reward_xp  # Assuming a `reward_xp` field on the quest model

    try:
        db.session.commit()
        return jsonify({"message": "Quest completed", "quest_id": quest_id, "user_currency": user.currency, "user_xp": user.experience_points})
    except Exception as e:
        db.session.rollback()  # Rollback in case of any failure
        return jsonify({"error": "An error occurred while completing the quest", "details": str(e)}), 500