from flask import Blueprint, request, jsonify
from datetime import datetime
from models import UserQuest, Quest, db
from sqlalchemy.exc import SQLAlchemyError

user_quests_bp = Blueprint('user_quests', __name__)

PROGRESS_COMPLETE_THRESHOLD = 100

def handle_error(message, status_code):
    response = jsonify({'error': message})
    response.status_code = status_code
    return response

@user_quests_bp.route('/update', methods=['POST'])
def update_user_quest():
    data = request.get_json()
    user_quest_id = data.get('user_quest_id')
    progress = data.get('progress')
    
    if not user_quest_id or progress is None:
        return handle_error('Missing required fields: user_quest_id and progress', 400)

    user_quest = UserQuest.query.get(user_quest_id)
    if not user_quest:
        return handle_error('User quest not found', 404)

    try:
        user_quest.progress = progress
        # Automatically mark quest as completed if progress reaches or exceeds the threshold
        if progress >= PROGRESS_COMPLETE_THRESHOLD:
            user_quest.status = 'completed'
            user_quest.completed_at = datetime.utcnow()
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_error('Database error occurred', 500)

    return jsonify({'message': 'User quest progress updated', 'user_quest_id': user_quest.id}), 200
