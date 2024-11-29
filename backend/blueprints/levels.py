from flask import Blueprint, jsonify
from services.game_service import GameService

levels_bp = Blueprint('levels_bp', __name__)

@levels_bp.route('/list', methods=['GET'])
def list_levels():
    levels = GameService.get_all_levels()
    return jsonify(levels), 200
