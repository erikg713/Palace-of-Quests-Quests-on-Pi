from flask import Blueprint, request, jsonify
from models import Inventory, User
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/items', methods=['GET'])
def get_items():
    items = Inventory.query.all()
    return jsonify([{'id': item.id, 'name': item.item_name, 'type': item.item_type, 'price': item.price} for item in items])

@marketplace_bp.route('/purchase', methods=['POST'])
@jwt_required()
def purchase_item():
    user_id = get_jwt_identity()
    data = request.json
    item_id = data['item_id']
    
    item = Inventory.query.get(item_id)
    if item and item.user_id != user_id:
        # Transfer ownership
        item.user_id = user_id
        db.session.commit()
        return jsonify(message="Item purchased successfully"), 200
    return jsonify(message="Purchase failed"), 400

@marketplace_bp.route('/bridge-to-eth', methods=['POST'])
@jwt_required()
def bridge_to_eth():
    # Dummy function for cross-chain bridge demonstration
    data = request.json
    item_id = data['item_id']
    # Code here would call smart contracts or external APIs to move assets to Ethereum network
    return jsonify(message=f"Item {item_id} bridged to Ethereum network successfully"), 200
