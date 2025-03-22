from flask import Blueprint, request, jsonify
from models import Quest, db

quests_bp = Blueprint('quests', __name__)

@quests_bp.route('/', methods=['GET'])
def get_quests():
    quests = Quest.query.all()
    quest_list = []
    for quest in quests:
        quest_list.append({
            "id": quest.id,
            "title": quest.title,
            "description": quest.description,
            "reward": quest.reward,
            "level_required": quest.level_required,
            "created_at": quest.created_at.isoformat()
        })
    return jsonify({"quests": quest_list}), 200

@quests_bp.route('/start', methods=['POST'])
def start_quest():
    data = request.get_json()
    quest_id = data.get('quest_id')
    user_id = data.get('user_id')  # In a production environment, this would be derived from authentication
    
    if not quest_id or not user_id:
        return jsonify({"error": "Missing required fields: quest_id and user_id"}), 400
    
    quest = Quest.query.get(quest_id)
    if not quest:
        return jsonify({"error": "Quest not found"}), 404

    # Simulate starting a quest.
    # In production, create a record in a QuestProgress/UserQuest model
    return jsonify({"message": f"User {user_id} started quest '{quest.title}'"}), 200

@quests_bp.route('/progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    quest_id = data.get('quest_id')
    user_id = data.get('user_id')
    progress = data.get('progress')  # e.g., progress percentage or milestones
    
    if not quest_id or not user_id or progress is None:
        return jsonify({"error": "Missing required fields: quest_id, user_id, and progress"}), 400

    # Simulate updating quest progress.
    # In production, update the quest progress record accordingly.
    return jsonify({"message": f"User {user_id}'s progress for quest {quest_id} updated to {progress}%"}), 200
