from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from models import Quest, db
from middleware.roles import requires_role

import logging

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)

# Helpers
def get_json_field(data, field, required=True):
    value = data.get(field)
    if required and value is None:
        raise ValueError(f"Missing required field: {field}")
    return value

def get_quest_or_404(quest_id):
    quest = Quest.query.get(quest_id)
    if not quest:
        return None, jsonify({"error": "Quest not found"}), 404
    return quest, None, None

# Routes
@admin_bp.route('/quest/create', methods=['POST'])
@requires_role('admin')
def create_quest():
    """
    Create a new quest.
    Expects JSON with: title, description, reward, level_required.
    """
    try:
        data = request.get_json()
        title = get_json_field(data, 'title')
        description = get_json_field(data, 'description')
        reward = get_json_field(data, 'reward')
        level_required = get_json_field(data, 'level_required')

        new_quest = Quest(
            title=title,
            description=description,
            reward=reward,
            level_required=level_required,
            created_at=datetime.utcnow()
        )
        db.session.add(new_quest)
        db.session.commit()
        logger.info(f"Quest created: {new_quest.id}")
        return jsonify({"message": "Quest created successfully", "quest_id": new_quest.id}), 201
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"DB error on create: {e}")
        return jsonify({"error": "Database error occurred"}), 500

@admin_bp.route('/quest/update', methods=['PUT'])
@requires_role('admin')
def update_quest():
    """
    Update a quest. quest_id is required, other fields optional.
    """
    try:
        data = request.get_json()
        quest_id = get_json_field(data, 'quest_id')
        quest, error_resp, status = get_quest_or_404(quest_id)
        if not quest:
            return error_resp, status

        # Only update provided fields
        for field in ['title', 'description', 'reward', 'level_required']:
            if field in data:
                setattr(quest, field, data[field])
        db.session.commit()
        logger.info(f"Quest updated: {quest.id}")
        return jsonify({"message": "Quest updated successfully", "quest_id": quest.id}), 200
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"DB error on update: {e}")
        return jsonify({"error": "Database error occurred"}), 500

@admin_bp.route('/quest/delete', methods=['DELETE'])
@requires_role('admin')
def delete_quest():
    """
    Delete a quest by quest_id.
    """
    try:
        data = request.get_json()
        quest_id = get_json_field(data, 'quest_id')
        quest, error_resp, status = get_quest_or_404(quest_id)
        if not quest:
            return error_resp, status

        db.session.delete(quest)
        db.session.commit()
        logger.info(f"Quest deleted: {quest_id}")
        return jsonify({"message": "Quest deleted successfully", "quest_id": quest_id}), 200
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"DB error on delete: {e}")
        return jsonify({"error": "Database error occurred"}), 500
