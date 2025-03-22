from flask import Blueprint, request, jsonify
from models import Quest, db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/quest/create', methods=['POST'])
def create_quest():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    reward = data.get('reward')
    level_required = data.get('level_required')

    if not title or not description or reward is None or level_required is None:
        return jsonify({"error": "Missing required fields: title, description, reward, and level_required"}), 400

    new_quest = Quest(
        title=title,
        description=description,
        reward=reward,
        level_required=level_required,
        created_at=datetime.utcnow()
    )
    db.session.add(new_quest)
    db.session.commit()

    return jsonify({"message": "Quest created successfully", "quest_id": new_quest.id}), 201

@admin_bp.route('/quest/update', methods=['PUT'])
def update_quest():
    data = request.get_json()
    quest_id = data.get('quest_id')
    if not quest_id:
        return jsonify({"error": "Missing required field: quest_id"}), 400

    quest = Quest.query.get(quest_id)
    if not quest:
        return jsonify({"error": "Quest not found"}), 404

    # Update fields if provided; otherwise, keep the existing values
    quest.title = data.get('title', quest.title)
    quest.description = data.get('description', quest.description)
    quest.reward = data.get('reward', quest.reward)
    quest.level_required = data.get('level_required', quest.level_required)
    db.session.commit()

    return jsonify({"message": "Quest updated successfully", "quest_id": quest.id}), 200

@admin_bp.route('/quest/delete', methods=['DELETE'])
def delete_quest():
    data = request.get_json()
    quest_id = data.get('quest_id')
    if not quest_id:
        return jsonify({"error": "Missing required field: quest_id"}), 400

    quest = Quest.query.get(quest_id)
    if not quest:
        return jsonify({"error": "Quest not found"}), 404

    db.session.delete(quest)
    db.session.commit()
    return jsonify({"message": "Quest deleted successfully", "quest_id": quest_id}), 200
