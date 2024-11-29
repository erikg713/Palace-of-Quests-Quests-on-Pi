from flask import Blueprint, request, jsonify
from app.models import db, Skills, PlayerSkills

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/api/skills', methods=['GET'])
def get_skills():
    skills = Skills.query.all()
    return jsonify([skill.to_dict() for skill in skills])

@skills_bp.route('/api/player/<int:user_id>/skills/<int:skill_id>/upgrade', methods=['POST'])
def upgrade_skill(user_id, skill_id):
    data = request.json
    player_skill = PlayerSkills.query.filter_by(user_id=user_id, skill_id=skill_id).first()
    skill = Skills.query.get(skill_id)

    if player_skill.current_level >= skill.max_level:
        return jsonify({"message": "Skill is already at max level"}), 400

    # Deduct coins and XP
    coins_spent = data['coins_spent']
    xp_used = data['xp_used']
    # Assume player stats validation is done here

    player_skill.current_level += 1
    db.session.commit()

    return jsonify({"message": "Skill upgraded successfully", "current_level": player_skill.current_level})
