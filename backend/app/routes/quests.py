from flask import Blueprint, request, jsonify
from models import Quest, db
from sqlalchemy.exc import SQLAlchemyError

quests_bp = Blueprint('quests', __name__)

@quests_bp.route('/', methods=['GET'])
def get_quests():
    """Fetch all quests."""
    try:
        quests = (
            db.session.query(
                Quest.id,
                Quest.title,
                Quest.description,
                Quest.reward,
                Quest.level_required,
                Quest.created_at
            ).all()
        )
        return jsonify({
            "quests": [
                {
                    "id": q.id,
                    "title": q.title,
                    "description": q.description,
                    "reward": q.reward,
                    "level_required": q.level_required,
                    "created_at": q.created_at.isoformat()
                }
                for q in quests
            ]
        }), 200
    except SQLAlchemyError:
        return jsonify({"error": "Failed to fetch quests."}), 500

@quests_bp.route('/start', methods=['POST'])
def start_quest():
    """Start a quest for a user."""
    data = request.get_json(silent=True) or {}
    quest_id = data.get('quest_id')
    user_id = data.get('user_id')  # TODO: Replace with authentication

    if not quest_id or not user_id:
        return jsonify({"error": "quest_id and user_id are required."}), 400

    try:
        quest = Quest.query.get(quest_id)
        if not quest:
            return jsonify({"error": "Quest not found."}), 404

        # TODO: Record quest start in user progress table
        return jsonify({
            "message": f"User {user_id} started quest '{quest.title}'"
        }), 200
    except SQLAlchemyError:
        return jsonify({"error": "Failed to start quest."}), 500

@quests_bp.route('/progress', methods=['POST'])
def update_progress():
    """Update quest progress for a user."""
    data = request.get_json(silent=True) or {}
    quest_id = data.get('quest_id')
    user_id = data.get('user_id')
    progress = data.get('progress')

    if not all([quest_id, user_id]) or progress is None:
        return jsonify({
            "error": "quest_id, user_id, and progress are required."
        }), 400

    try:
        # TODO: Persist progress update to DB
        return jsonify({
            "message": f"User {user_id}'s progress for quest {quest_id} updated to {progress}%"
        }), 200
    except SQLAlchemyError:
        return jsonify({"error": "Failed to update progress."}), 500
