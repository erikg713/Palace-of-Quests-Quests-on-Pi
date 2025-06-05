from flask import Blueprint, request, jsonify
from models import Quest, db
from datetime import datetime
from middleware.roles import requires_role

admin_bp = Blueprint('admin', __name__)

def validate_request(data, required_fields):
    """Helper function to validate request payload"""
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400
    return None

@admin_bp.route('/quest/create', methods=['POST'])
@requires_role('admin')
def create_quest():
    data = request.get_json()
    validation_error = validate_request(data, ['title', 'description', 'reward', 'level_required'])
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    try:
        new_quest = Quest(
            title=data['title'],
            description=data['description'],
            reward=data['reward'],
            level_required=data['level_required'],
            created_at=datetime.utcnow()
        )
        db.session.add(new_quest)
        db.session.commit()
        return jsonify({"message": "Quest created successfully", "quest_id": new_quest.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create quest", "details": str(e)}), 500

@admin_bp.route('/quest/update', methods=['PUT'])
@requires_role('admin')
def update_quest():
    data = request.get_json()
    validation_error = validate_request(data, ['quest_id'])
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    try:
        quest = Quest.query.get(data['quest_id'])
        if not quest:
            return jsonify({"error": "Quest not found"}), 404

        # Update fields if provided
        quest.title = data.get('title', quest.title)
        quest.description = data.get('description', quest.description)
        quest.reward = data.get('reward', quest.reward)
        quest.level_required = data.get('level_required', quest.level_required)
        db.session.commit()

        return jsonify({"message": "Quest updated successfully", "quest_id": quest.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update quest", "details": str(e)}), 500

@admin_bp.route('/quest/delete', methods=['DELETE'])
@requires_role('admin')
def delete_quest():
    data = request.get_json()
    validation_error = validate_request(data, ['quest_id'])
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    try:
        quest = Quest.query.get(data['quest_id'])
        if not quest:
            return jsonify({"error": "Quest not found"}), 404

        db.session.delete(quest)
        db.session.commit()
        return jsonify({"message": "Quest deleted successfully", "quest_id": data['quest_id']}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete quest", "details": str(e)}), 500
