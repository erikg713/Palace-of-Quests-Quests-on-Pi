from flask import Blueprint, request, jsonify
from models import User, Transaction, db
from sqlalchemy.exc import SQLAlchemyError

economy_bp = Blueprint("economy", __name__)

# --- Constants ---
_COMPLETED_STATUS = "completed"


@economy_bp.route("/balance", methods=["GET"])
def get_balance():
    """
    GET /balance?user_id=<user_id>
    Returns the balance for a specific user.
    """
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify(error="Missing or invalid 'user_id' parameter."), 400

    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify(error="User not found."), 404
        return jsonify(user_id=user.id, balance=user.balance), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error="Database error occurred."), 500


@economy_bp.route("/earnings", methods=["GET"])
def get_earnings():
    """
    GET /earnings
    Returns the total sum of completed transaction amounts.
    """
    try:
        total = (
            db.session.query(db.func.coalesce(db.func.sum(Transaction.amount), 0.0))
            .filter_by(status=_COMPLETED_STATUS)
            .scalar()
        )
        # Always return float for frontend consistency
        return jsonify(total_earnings=float(total)), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(error="Database error occurred."), 500
