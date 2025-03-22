from flask import Blueprint, request, jsonify
from datetime import datetime
from models import UserQuest, Quest, db

user_quests_bp = Blueprint('user_quests', __name__)

@user_quests_bp.route('/start', methods=['POST'])
def start_user_quest():
    data = request.get_json()
    user_id = data.get('user_id')
    quest_id = data.get('quest_id')
    
    if not user_id or not quest_id:
        return jsonify({'error': 'Missing required fields: user_id and quest_id'}), 400

    # Verify the quest exists
    quest = Quest.query.get(quest_id)
    if not quest:
        return jsonify({'error': 'Quest not found'}), 404

    # Check if a UserQuest already exists for this user and quest (prevent duplicates)
    existing = UserQuest.query.filter_by(user_id=user_id, quest_id=quest_id).first()
    if existing:
        return jsonify({'error': 'Quest already started for this user'}), 400

    new_user_quest = UserQuest(user_id=user_id, quest_id=quest_id)
    db.session.add(new_user_quest)
    db.session.commit()

    return jsonify({'message': 'User quest started', 'user_quest_id': new_user_quest.id}), 201

@user_quests_bp.route('/update', methods=['POST'])
def update_user_quest():
    data = request.get_json()
    user_quest_id = data.get('user_quest_id')
    progress = data.get('progress')
    
    if not user_quest_id or progress is None:
        return jsonify({'error': 'Missing required fields: user_quest_id and progress'}), 400

    user_quest = UserQuest.query.get(user_quest_id)
    if not user_quest:
        return jsonify({'error': 'User quest not found'}), 404

    user_quest.progress = progress
    # Automatically mark quest as completed if progress reaches or exceeds 100%
    if progress >= 100:
        user_quest.status = 'completed'
        user_quest.completed_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'User quest progress updated', 'user_quest_id': user_quest.id}), 200

@user_quests_bp.route('/', methods=['GET'])
def get_user_quests():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing required parameter: user_id'}), 400

    user_quests = UserQuest.query.filter_by(user_id=user_id).all()
    result = []
    for uq in user_quests:
        result.append({
            'user_quest_id': uq.id,
            'quest_id': uq.quest_id,
            'progress': uq.progress,
            'status': uq.status,
            'started_at': uq.started_at.isoformat(),
            'completed_at': uq.completed_at.isoformat() if uq.completed_at else None
        })

    return jsonify({'user_id': user_id, 'quests': result}), 200
