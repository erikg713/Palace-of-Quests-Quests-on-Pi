from flask import Blueprint, request, jsonify
from app.models import Avatar, db

avatar_bp = Blueprint("avatar", __name__)

@avatar_bp.route("/get_avatar", methods=["GET"])
def get_avatar():
    # Assume current user has ID of 1 for simplicity
    avatar = Avatar.query.filter_by(user_id=1).first()
    return jsonify(avatar.to_dict())

@avatar_bp.route("/upgrade_avatar", methods=["POST"])
def upgrade_avatar():
    avatar = Avatar.query.filter_by(user_id=1).first()
    if avatar.level < 250:
        avatar.level += 1
        db.session.commit()
    return jsonify(avatar.to_dict())

from flask import Blueprint, request, jsonify
from app.models import Avatar, db

avatar_bp = Blueprint("avatar", __name__)

@avatar_bp.route("/customize_avatar", methods=["POST"])
def customize_avatar():
    data = request.get_json()
    attributes = data.get("attributes")
    avatar = Avatar.query.filter_by(user_id=1).first()  # Replace with actual user retrieval

    for attribute, value in attributes.items():
        setattr(avatar, attribute, value)

    db.session.commit()
    return jsonify(avatar.to_dict())

from flask import Blueprint, request, jsonify
from app.models import Avatar, db

avatar_bp = Blueprint("avatar", __name__)

@avatar_bp.route("/customize_avatar", methods=["POST"])
def customize_avatar():
    data = request.get_json()
    attribute = data.get("attribute")
    value = data.get("value")
    avatar = Avatar.query.filter_by(user_id=1).first()  # Replace with actual user retrieval

    if attribute == "outfit":
        avatar.outfit = value
    elif attribute == "helmet":
        avatar.helmet = value
    db.session.commit()
    return jsonify(avatar.to_dict())

from flask import Blueprint, request, jsonify
from app.models import Item, User, db

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/sell_item/<int:item_id>", methods=["POST"])
def sell_item(item_id):
    item = Item.query.get(item_id)
    user = User.query.get(1)  # Replace with actual user retrieval

    if item and not item.equipped:
        sell_price = item.value  # Define a `value` attribute in Item for sell price
        user.currency += sell_price  # Add sell price to user's currency
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item sold", "currency": user.currency, "items": [i.to_dict() for i in user.items]})
    else:
        return jsonify({"error": "Item not found or is currently equipped"}), 400
