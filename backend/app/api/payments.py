"""Payment Endpoints"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Transaction
from .utils import api_response, api_error

api_payments = Blueprint('api_payments', __name__)

@api_payments.route('/initiate', methods=['POST'])
@jwt_required()
def initiate_payment():
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    amount = data.get('amount')
    description = data.get('description')

    if not amount or not description:
        return api_error("amount and description are required", 400)
    
    # Simulate Pi payment initiation
    transaction = Transaction(sender_id=user_id, amount=amount, description=description)
    db.session.add(transaction)
    db.session.commit()

    return api_response(message="Payment initiated", data=transaction.to_dict(), status_code=201)

@api_payments.route('/verify', methods=['POST'])
@jwt_required()
def verify_payment():
    data = request.get_json() or {}
    payment_id = data.get('paymentId')
    if not payment_id:
        return api_error('paymentId is required', 400)

    transaction = Transaction.query.filter_by(id=payment_id).first()
    if not transaction:
        return api_error('Payment not found', 404)

    # Simulate verification logic
    verified = True  # Replace with real check
    return api_response(message="Payment verified" if verified else "Payment not verified", data={'verified': verified})
@app.route("/pay", methods=["POST"])
def process_payment():
    data = request.json
    payment_id = data.get("payment_id")
    
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}
    response = requests.post(f"{PI_AUTH_URL}/payments/{payment_id}", headers=headers)
    
    if response.status_code == 200:
        payment_data = response.json()
        return jsonify({"status": "success", "payment": payment_data}), 200
    else:
        return jsonify({"error": "Payment failed"}), 400
