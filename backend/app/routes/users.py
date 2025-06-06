from flask import Blueprint, request, jsonify
from models import User, db
import logging

users_bp = Blueprint('users', __name__)

logger = logging.getLogger(__name__)

@users_bp.route('/inventory', methods=['GET'])
def get_inventory():
    """
    Get the inventory for a user.
    Expects:
        user_id (int): The user's ID as a query parameter.
    Returns:
        JSON response with the user's inventory or an error.
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        logger.warning("Missing or invalid user_id parameter.")
        return jsonify({"error": "Missing or invalid user_id parameter."}), 400

    user = User.query.get(user_id)
    if not user:
        logger.info(f"User not found: {user_id}")
        return jsonify({"error": "User not found."}), 404

    # Assuming a relationship: User.inventory_items (define this in your model)
    inventory = [
        {
            "item_id": item.id,
            "name": item.name,
            "quantity": item.quantity,
        }
        for item in getattr(user, "inventory_items", [])
    ]

    return jsonify({
        "user_id": user.id,
        "inventory": inventory,
    }), 200
