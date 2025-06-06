from flask import Blueprint, request, jsonify
from datetime import datetime
from models import UserQuest, db
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum

user_quests_bp = Blueprint('user_quests', __name__)

PROGRESS_COMPLETE_THRESHOLD = 100

class UserQuestStatus(Enum):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class UserQuestError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def handle_error(error):
    return jsonify({'error': error.message}), error.status_code

def update_user_quest_in_db(user_quest_id, progress):
    user_quest = UserQuest.query.get(user_quest_id)
    if user_quest is None:
        raise UserQuestError('User quest not found', 404)

    # Only update if progress changes
    updated = False
    if user_quest.progress != progress:
        user_quest.progress = progress
        updated = True

    if progress >= PROGRESS_COMPLETE_THRESHOLD and user_quest.status != UserQuestStatus.COMPLETED.value:
        user_quest.status = UserQuestStatus.COMPLETED.value
        user_quest.completed_at = datetime.utcnow()
        updated = True

    if updated:
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise UserQuestError('Database error occurred', 500)
    return user_quest

@user_quests_bp.route('/update', methods=['POST'])
def update_user_quest():
    data = request.get_json(silent=True) or {}
    user_quest_id = data.get('user_quest_id')
    progress = data.get('progress')

    if not user_quest_id or progress is None:
        return handle_error(UserQuestError('Missing required fields: user_quest_id and progress'))

    try:
        user_quest = update_user_quest_in_db(user_quest_id, progress)
    except UserQuestError as e:
        return handle_error(e)

    return jsonify({
        'message': 'User quest progress updated',
        'user_quest_id': user_quest.id,
        'progress': user_quest.progress,
        'status': user_quest.status,
        'completed_at': user_quest.completed_at.isoformat() if user_quest.completed_at else None
    }), 200
