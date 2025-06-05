"""Quest Endpoints"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Quest, User, QuestProgress
from .utils import api_response, api_error

api_quests = Blueprint('api_quests', __name__)

@api_quests.route('/', methods=['GET'])
@jwt_required()
def list_quests():
    quests = Quest.query.all()
    return api_response(data=[q.to_dict() for q in quests])

@api_quests.route('/start', methods=['POST'])
@jwt_required()
def start_quest():
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    quest_id = data.get('quest_id')
    if not quest_id:
        return api_error('Quest ID is required', 400)

    quest = Quest.query.get(quest_id)
    user = User.query.get(user_id)
    if not quest or not user:
        return api_error('Invalid quest or user', 404)

    # Prevent duplicate quest progress
    if QuestProgress.query.filter_by(user_id=user_id, quest_id=quest_id).first():
        return api_error('Quest already started', 409)

    progress = QuestProgress(user_id=user_id, quest_id=quest_id, progress=0.0, completed=False)
    db.session.add(progress)
    db.session.commit()
    return api_response(message="Quest started", data=progress.to_dict(), status_code=201)

@api_quests.route('/progress', methods=['POST'])
@jwt_required()
def update_progress():
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    quest_id = data.get('quest_id')
    progress_value = data.get('progress')
    if not quest_id or progress_value is None:
        return api_error('quest_id and progress are required', 400)

    progress = QuestProgress.query.filter_by(user_id=user_id, quest_id=quest_id).first()
    if not progress:
        return api_error('No active quest progress found', 404)

    progress.progress = float(progress_value)
    if progress.progress >= 100.0:
        progress.completed = True
    db.session.commit()
    return api_response(message="Quest progress updated", data=progress.to_dict())
