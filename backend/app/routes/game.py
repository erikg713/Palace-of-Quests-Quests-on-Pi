from flask import Blueprint, request, jsonify
from app.models import Quest, db

game_bp = Blueprint("game", __name__)

@game_bp.route("/quests", methods=["GET"])
def get_quests():
    quests = Quest.query.all()
    return jsonify([quest.to_dict() for quest in quests])

@game_bp.route("/complete_quest/<int:quest_id>", methods=["POST"])
def complete_quest(quest_id):
    quest = Quest.query.get(quest_id)
    if quest:
        quest.is_completed = True
        db.session.commit()
        return jsonify({"message": "Quest completed", "quest_id": quest_id})
    else:
        return jsonify({"error": "Quest not found"}), 404
