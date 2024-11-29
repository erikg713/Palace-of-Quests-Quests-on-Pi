from flask import Blueprint, request, jsonify
from services.game_service import GameService
from flask_jwt_extended import jwt_required, get_jwt_identity

progress_bp = Blueprint('progress_bp', __name__)

@progress_bp.route('/update', methods=['POST'])
@jwt_required()
def update_progress():
    user_id = get_jwt_identity()
    data = request.get_json()
    progress = data['progress']
    if GameService.update_user_progress(user_id, progress):
        return jsonify({"message": "Progress updated"}), 200
    return jsonify({"error": "Failed to update progress"}), 400
