from flask import Blueprint, jsonify
from app.models import LevelReward, Avatar, Item, db

level_bp = Blueprint("level", __name__)

# Route to get level rewards for a specific level
@level_bp.route("/level_rewards/<int:level>", methods=["GET"])
def get_level_rewards(level):
    reward = LevelReward.query.filter_by(level=level).first()
    if reward:
        return jsonify(reward.to_dict())
    else:
        return jsonify({"error": "No rewards found for this level"}), 404

# Route to upgrade the avatar's level and apply rewards
@level_bp.route("/upgrade_level", methods=["POST"])
def upgrade_level():
    avatar = Avatar.query.filter_by(user_id=1).first()  # Replace with dynamic user retrieval
    if not avatar:
        return jsonify({"error": "Avatar not found"}), 404
    
    if avatar.level < 250:
        avatar.level += 1  # Upgrade level
        level_reward = LevelReward.query.filter_by(level=avatar.level).first()

        if level_reward:
            # Apply rewards to the avatar
            avatar.stat_points += level_reward.stat_boost

            # Add the item to the avatar's inventory
            new_item = Item(name=level_reward.item_unlock, avatar_id=avatar.id)
            db.session.add(new_item)

        db.session.commit()
        return jsonify({"message": f"Upgraded to level {avatar.level}", "reward": level_reward.to_dict()})
    return jsonify({"error": "Maximum level reached"}), 400