from flask import Blueprint, request, jsonify
from models import Item, User, Transaction, db
import uuid

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/list', methods=['POST'])
def list_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')
    seller_id = data.get('seller_id')

    if not name or price is None or not seller_id:
        return jsonify({"error": "Missing required fields: name, price, seller_id"}), 400

    new_item = Item(name=name, description=description, price=price, seller_id=seller_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Item listed successfully", "item_id": new_item.id}), 201

@marketplace_bp.route('/buy', methods=['POST'])
def buy_item():
    data = request.get_json()
    item_id = data.get('item_id')
    buyer_id = data.get('buyer_id')

    if not item_id or not buyer_id:
        return jsonify({"error": "Missing required fields: item_id, buyer_id"}), 400

    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    if item.status != 'available':
        return jsonify({"error": "Item is not available for purchase"}), 400

    # Simulate a purchase by updating item status and buyer info
    item.buyer_id = buyer_id
    item.status = 'sold'
    db.session.commit()

    # Record transaction (simulate escrow release, etc.)
    new_transaction = Transaction(
        sender_id=buyer_id,
        receiver_id=item.seller_id,
        amount=item.price,
        status='completed'
    )
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": f"Item {item_id} purchased successfully", "transaction_id": new_transaction.id}), 200

@marketplace_bp.route('/trade', methods=['POST'])
def trade_item():
    data = request.get_json()
    item_id = data.get('item_id')
    seller_id = data.get('seller_id')
    buyer_id = data.get('buyer_id')
    escrow = data.get('escrow', True)  # In a real-world scenario, you'd implement escrow logic

    if not item_id or not seller_id or not buyer_id:
        return jsonify({"error": "Missing required fields: item_id, seller_id, buyer_id"}), 400

    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    if item.status != 'available':
        return jsonify({"error": "Item is not available for trade"}), 400

    # For demonstration, we simulate an escrow trade by marking item as 'pending'
    item.status = 'pending'
    db.session.commit()

    # Create a transaction record with 'pending' status
    trade_transaction = Transaction(
        sender_id=buyer_id,
        receiver_id=seller_id,
        amount=item.price,
        status='pending'
    )
    db.session.add(trade_transaction)
    db.session.commit()

    return jsonify({
        "message": f"Trade initiated for item {item_id}. Escrow in place.",
        "transaction_id": trade_transaction.id
    }), 200
