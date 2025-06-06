from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import Item, User, Transaction, db

marketplace_bp = Blueprint('marketplace', __name__)

def error_response(message, status=400, code=None, details=None):
    """Standardized error response."""
    resp = {"error": message}
    if code:
        resp["code"] = code
    if details:
        resp["details"] = details
    return jsonify(resp), status

def validate_positive_number(value, field):
    """Validate that a value is a positive number."""
    try:
        val = float(value)
        return val > 0
    except (TypeError, ValueError):
        return False

def get_item_or_404(item_id):
    """Fetch an item or return a 404 error."""
    item = Item.query.get(item_id)
    if not item:
        return None, error_response("Item not found", 404, code="ITEM_NOT_FOUND")
    return item, None

@marketplace_bp.route('/list', methods=['POST'])
def list_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')
    seller_id = data.get('seller_id')

    if not name or price is None or not seller_id:
        return error_response("Missing required fields: name, price, seller_id", code="MISSING_FIELDS")
    if not validate_positive_number(price, "price"):
        return error_response("Price must be a positive number", code="INVALID_PRICE")
    try:
        new_item = Item(
            name=name,
            description=description,
            price=price,
            seller_id=seller_id,
            status='available'
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item listed successfully", "item_id": new_item.id}), 201
    except SQLAlchemyError as exc:
        db.session.rollback()
        return error_response("Database error while listing item", 500, code="DB_ERROR", details=str(exc))

@marketplace_bp.route('/buy', methods=['POST'])
def buy_item():
    data = request.get_json()
    item_id = data.get('item_id')
    buyer_id = data.get('buyer_id')

    if not item_id or not buyer_id:
        return error_response("Missing required fields: item_id, buyer_id", code="MISSING_FIELDS")

    item, err = get_item_or_404(item_id)
    if err:
        return err

    if item.status != 'available':
        return error_response("Item is not available for purchase", code="NOT_AVAILABLE")

    # Optionally: Validate buyer exists and has enough balance, etc.

    try:
        item.buyer_id = buyer_id
        item.status = 'sold'
        db.session.commit()

        new_transaction = Transaction(
            sender_id=buyer_id,
            receiver_id=item.seller_id,
            amount=item.price,
            status='completed'
        )
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({
            "message": f"Item {item_id} purchased successfully",
            "transaction_id": new_transaction.id
        }), 200
    except SQLAlchemyError as exc:
        db.session.rollback()
        return error_response("Database error during purchase", 500, code="DB_ERROR", details=str(exc))

@marketplace_bp.route('/trade', methods=['POST'])
def trade_item():
    data = request.get_json()
    item_id = data.get('item_id')
    seller_id = data.get('seller_id')
    buyer_id = data.get('buyer_id')
    escrow = data.get('escrow', True)

    if not item_id or not seller_id or not buyer_id:
        return error_response("Missing required fields: item_id, seller_id, buyer_id", code="MISSING_FIELDS")

    item, err = get_item_or_404(item_id)
    if err:
        return err

    if item.status != 'available':
        return error_response("Item is not available for trade", code="NOT_AVAILABLE")

    try:
        item.status = 'pending'
        db.session.commit()

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
    except SQLAlchemyError as exc:
        db.session.rollback()
        return error_response("Database error during trade", 500, code="DB_ERROR", details=str(exc))
