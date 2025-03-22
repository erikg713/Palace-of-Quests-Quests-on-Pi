from flask import Blueprint, request, jsonify
from models import User, Transaction, db

economy_bp = Blueprint('economy', __name__)

@economy_bp.route('/balance', methods=['GET'])
def get_balance():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing required parameter: user_id"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"user_id": user.id, "balance": user.balance}), 200

@economy_bp.route('/earnings', methods=['GET'])
def get_earnings():
    # Sum of all completed transactions (this simulates the total earnings)
    total_earnings = db.session.query(db.func.sum(Transaction.amount))\
        .filter(Transaction.status == 'completed').scalar() or 0.0
    return jsonify({"total_earnings": total_earnings}), 200
