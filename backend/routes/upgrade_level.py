from flask import Blueprint, jsonify
from app.models import Avatar, LevelReward, Item, db

level_bp = Blueprint("level", __name__)

@level_bp.route("/upgrade_level", methods=["POST"])
def upgrade_level():
    avatar = Avatar.query.filter_by(user_id=1).first()  # Example user_id=1
    if avatar.level < 250:
        avatar.level += 1
        level_reward = LevelReward.query.filter_by(level=avatar.level).first()

        if level_reward:
            # Apply rewards to avatar (e.g., boost stats, add items)
            avatar.stat_points += level_reward.stat_boost
            new_item = Item(name=level_reward.item_unlock, avatar_id=avatar.id)
            db.session.add(new_item)

        db.session.commit()
        return jsonify({"message": f"Upgraded to level {avatar.level}", "reward": level_reward.to_dict()})
    return jsonify({"error": "Maximum level reached"}), 400