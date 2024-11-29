from flask import Blueprint, request, jsonify
from app.models import Item, User, db

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/sell_item/<int:item_id>", methods=["POST"])
def sell_item(item_id):
    item = Item.query.get(item_id)
    if item and not item.equipped:
        #

@inventory_bp.route("/upgrade_item/<int:item_id>", methods=["POST"])
def upgrade_item(item_id):
    item = Item.query.get(item_id)
    upgrade_cost = item.upgrade_level * 10  # Example upgrade cost calculation

    user = User.query.get(1)  # Replace with actual user retrieval
    if user.currency >= upgrade_cost:
        user.currency -= upgrade_cost
        item.upgrade_level += 1
        db.session.commit()
        return jsonify({"message": "Item upgraded", "item": item.to_dict(), "currency": user.currency})
    else:
        return jsonify({"error": "Insufficient currency"}), 400
