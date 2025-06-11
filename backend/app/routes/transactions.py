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
from flask import Blueprint, request, jsonify
from decimal import Decimal
from app.extensions import db
from app.models.transaction import Transaction, TransactionType
from app.models.user import User
from app.core.exceptions import ValidationError, InsufficientFundsError

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')


@transactions_bp.route('/transfer', methods=['POST'])
def create_transfer():
    try:
        data = request.get_json()
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        amount = Decimal(data.get('amount'))
        description = data.get('description')

        if not sender_id or not receiver_id or not amount:
            return jsonify({'error': 'Missing required fields'}), 400

        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)

        if not sender or not receiver:
            return jsonify({'error': 'Invalid sender or receiver ID'}), 404

        txn = Transaction.create_transfer(sender, receiver, amount, description)
        db.session.add(txn)
        db.session.commit()

        return jsonify({'transaction': txn.to_dict()}), 201

    except (ValidationError, InsufficientFundsError) as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'details': str(e)}), 500


@transactions_bp.route('/<txn_id>/process', methods=['POST'])
def process_transaction(txn_id):
    txn = Transaction.query.get(txn_id)
    if not txn:
        return jsonify({'error': 'Transaction not found'}), 404

    try:
        success = txn.process()
        db.session.commit()
        return jsonify({'transaction': txn.to_dict(include_sensitive=True), 'success': success}), 200
    except ValidationError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Processing failed', 'details': str(e)}), 500


@transactions_bp.route('/<txn_id>/refund', methods=['POST'])
def refund_transaction(txn_id):
    txn = Transaction.query.get(txn_id)
    if not txn:
        return jsonify({'error': 'Transaction not found'}), 404

    try:
        reason = request.json.get('reason', '')
        refund_txn = txn.refund(reason=reason)
        db.session.commit()
        return jsonify({'refund_transaction': refund_txn.to_dict()}), 201
    except ValidationError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Refund failed', 'details': str(e)}), 500


@transactions_bp.route('/<txn_id>/cancel', methods=['POST'])
def cancel_transaction(txn_id):
    txn = Transaction.query.get(txn_id)
    if not txn:
        return jsonify({'error': 'Transaction not found'}), 404

    try:
        reason = request.json.get('reason', '')
        txn.cancel(reason)
        db.session.commit()
        return jsonify({'transaction': txn.to_dict()}), 200
    except ValidationError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Cancellation failed', 'details': str(e)}), 500