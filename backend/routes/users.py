from flask import Blueprint, request, jsonify
from models import User, db

users_bp = Blueprint('users', __name__)

@users_bp.route('/inventory', methods=['GET'])
def get_inventory():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing required parameter: user_id"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Placeholder for inventory items.
    # In a full implementation, query a UserInventory table related to this user.
    inventory = []  
    
    return jsonify({"user_id": user.id, "inventory": inventory}), 200
