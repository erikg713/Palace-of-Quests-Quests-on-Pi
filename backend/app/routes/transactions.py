from flask import Blueprint, request, jsonify
from models import Transaction, db

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing required parameter: user_id"}), 400
    
    # Fetch transactions where the user is either the sender or receiver.
    transactions = Transaction.query.filter(
        (Transaction.sender_id == user_id) | (Transaction.receiver_id == user_id)
    ).all()
    
    result = []
    for tx in transactions:
        result.append({
            "id": tx.id,
            "sender_id": tx.sender_id,
            "receiver_id": tx.receiver_id,
            "amount": tx.amount,
            "status": tx.status,
            "created_at": tx.created_at.isoformat()
        })
    
    return jsonify({"user_id": user_id, "transactions": result}), 200
