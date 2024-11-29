from flask import Blueprint, request, jsonify
from app.models import Item, User, db

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/sell_item/<int:item_id>", methods=["POST"])
def sell_item(item_id):
    item = Item.query.get(item_id)
    if item and not item.equipped:
        user = User.query.get(1)  # Replace with actual user retrieval (e.g., from JWT token)
        
        # Define the item sell price (you can adjust this according to your model)
        sell_price = item.value  # Assuming 'value' is the price of the item
        
        # Add the item's value to the user's currency
        user.currency += sell_price
        
        # Remove the item from the database
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({"message": "Item sold", "currency": user.currency, "items": [i.to_dict() for i in user.items]})
    else:
        return jsonify({"error": "Item not found or is currently equipped"}), 400


@inventory_bp.route("/upgrade_item/<int:item_id>", methods=["POST"])
def upgrade_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    # Example upgrade cost calculation
    upgrade_cost = item.upgrade_level * 10  # Assuming 'upgrade_level' is a field for item upgrade
    
    user = User.query.get(1)  # Replace with actual user retrieval (e.g., from JWT token)
    if user.currency >= upgrade_cost:
        # Deduct currency from user and upgrade item
        user.currency -= upgrade_cost
        item.upgrade_level += 1
        
        # Optionally, you can add additional upgrade effects (e.g., increased stats, new abilities)
        db.session.commit()
        
        return jsonify({"message": "Item upgraded", "item": item.to_dict(), "currency": user.currency})
    else:
        return jsonify({"error": "Insufficient currency"}), 400