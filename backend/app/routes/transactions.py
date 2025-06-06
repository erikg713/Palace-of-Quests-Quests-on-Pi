from flask import Blueprint, request, jsonify, current_app
from models import Transaction, db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")

@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    """
    Retrieve transactions for a specific user.
    Expects 'user_id' as a query parameter.
    """
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        raise BadRequest("Missing or invalid required parameter: user_id (integer)")

    try:
        # Limit is set for safety—adjust as needed for production usage
        transactions = (
            Transaction.query
            .filter(
                (Transaction.sender_id == user_id) |
                (Transaction.receiver_id == user_id)
            )
            .order_by(Transaction.created_at.desc())
            .limit(100)
            .all()
        )
    except SQLAlchemyError as err:
        current_app.logger.error(f"DB error fetching transactions for user {user_id}: {err}")
        return jsonify({"error": "Database error occurred."}), 500

    result = [
        {
            "id": tx.id,
            "sender_id": tx.sender_id,
            "receiver_id": tx.receiver_id,
            "amount": float(tx.amount) if hasattr(tx.amount, "real") else tx.amount,
            "status": tx.status,
            "created_at": tx.created_at.isoformat()
        }
        for tx in transactions
    ]

    return jsonify({"user_id": user_id, "transactions": result}), 200
