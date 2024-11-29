from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_progress import UserProgress, db
from models.level import Level

level_bp = Blueprint("level", __name__)

@level_bp.route("/", methods=["GET"])
@jwt_required()
def get_progress():
    identity = get_jwt_identity()
    progress = UserProgress.query.filter_by(user_id=identity["id"]).first()

    if not progress:
        return jsonify({"message": "Progress not found"}), 404

    return jsonify({
        "current_level": progress.current_level,
        "xp": progress.xp
    })

@level_bp.route("/level-up", methods=["POST"])
@jwt_required()
def level_up():
    identity = get_jwt_identity()
    progress = UserProgress.query.filter_by(user_id=identity["id"]).first()
    if not progress:
        return jsonify({"message": "Progress not found"}), 404

    next_level = progress.current_level + 1
    level_data = Level.query.filter_by(level_number=next_level).first()
    
    if not level_data:
        return jsonify({"message": "Maximum level reached"}), 400

    if progress.xp >= level_data.xp_required:
        progress.current_level = next_level
        progress.xp -= level_data.xp_required
        db.session.commit()
        return jsonify({"message": "Level up successful"}), 200

    return jsonify({"message": "Not enough XP to level up"}), 400