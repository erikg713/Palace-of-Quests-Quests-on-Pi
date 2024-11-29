from flask import Blueprint, request, jsonify, g
from app.models import Avatar, Item, User, db

avatar_bp = Blueprint("avatar", __name__)

@avatar_bp.route("/get_avatar", methods=["GET"])
def get_avatar():
    # Retrieve the current user dynamically
    avatar = Avatar.query.filter_by(user_id=g.user.id).first()
    return jsonify(avatar.to_dict())

@avatar_bp.route("/upgrade_avatar", methods=["POST"])
def upgrade_avatar():
    avatar = Avatar.query.filter_by(user_id=g.user.id).first()
    if avatar.level < 250:
        avatar.level += 1
        db.session.commit()
    return jsonify(avatar.to_dict())

@avatar_bp.route("/customize_avatar", methods=["POST"])
def customize_avatar():
    data = request.get_json()
    avatar = Avatar.query.filter_by(user_id=g.user.id).first()  # Get current user avatar
    
    # Validate and update avatar attributes
    attribute = data.get("attribute")
    value = data.get("value")

    if attribute == "outfit":
        avatar.outfit = value
    elif attribute == "helmet":
        avatar.helmet = value
    else:
        return jsonify({"error": "Invalid attribute"}), 400

    db.session.commit()
    return jsonify(avatar.to_dict())


inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/sell_item/<int:item_id>", methods=["POST"])
def sell_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    user = User.query.filter_by(id=g.user.id).first()  # Get current user dynamically

    # Ensure item is not equipped
    if item.equipped:
        return jsonify({"error": "Item is currently equipped and cannot be sold"}), 400

    # Sell item
    sell_price = item.value
    user.currency += sell_price
    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "Item sold",
        "currency": user.currency,
        "items": [i.to_dict() for i in user.items]
    })