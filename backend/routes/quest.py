from flask import Blueprint, jsonify, request
from models import User, Quest, Reward
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity

quests_bp = Blueprint('quests', __name__)

@quests_bp.route('/start', methods=['POST'])
@jwt_required()
def start_quest():
    user_id = get_jwt_identity()
    data = request.json
    quest = Quest(user_id=user_id, name=data['quest_name'])
    db.session.add(quest)
    db.session.commit()
    return jsonify(message="Quest started"), 201

@quests_bp.route('/complete', methods=['POST'])
@jwt_required()
def complete_quest():
    user_id = get_jwt_identity()
    data = request.json
    quest = Quest.query.filter_by(id=data['quest_id'], user_id=user_id).first()
    if quest:
        # Mark quest as completed and add reward to user
        quest.is_completed = True
        db.session.commit()
        
        reward = Reward(user_id=user_id, type="PiToken", amount=50)  # Example reward
        db.session.add(reward)
        db.session.commit()
        
        return jsonify(message="Quest completed and reward added"), 200
    return jsonify(message="Quest not found"), 404
