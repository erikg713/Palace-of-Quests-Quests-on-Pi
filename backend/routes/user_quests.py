from flask import Blueprint, request, jsonify
from datetime import datetime
from models import UserQuest, Quest, db
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum

user_quests_bp = Blueprint('user_quests', __name__)

PROGRESS_COMPLETE_THRESHOLD = 100

class UserQuestStatus(Enum):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class UserQuestError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def handle_error(error):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response

def update_user_quest_in_db(user_quest_id, progress):
    user_quest = UserQuest.query.get(user_quest_id)
    if not user_quest:
        raise UserQuestError('User quest not found', 404)
    
    user_quest.progress = progress
    if progress >= PROGRESS_COMPLETE_THRESHOLD:
        user_quest.status = UserQuestStatus.COMPLETED.value
        user_quest.completed_at = datetime.utcnow()
    
    db.session.commit()
    return user_quest

@user_quests_bp.route('/update', methods=['POST'])
def update_user_quest():
    data = request.get_json()
    user_quest_id = data.get('user_quest_id')
    progress = data.get('progress')
    
    if not user_quest_id or progress is None:
        return handle_error(UserQuestError('Missing required fields: user_quest_id and progress', 400))
    
    try:
        user_quest = update_user_quest_in_db(user_quest_id, progress)
    except UserQuestError as e:
        return handle_error(e)
    except SQLAlchemyError as e:
        db.session.rollback()
        return handle_error(UserQuestError('Database error occurred', 500))

    return jsonify({'message': 'User quest progress updated', 'user_quest_id': user_quest.id}), 200
