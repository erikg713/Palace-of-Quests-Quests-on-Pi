from flask import Blueprint, request, jsonify
from app.utils.piAPI import approve_payment, complete_payment
import os

payments_bp = Blueprint("payments", __name__)

# Route to approve a payment
@payments_bp.route("/approve", methods=["POST"])
def approve():
    payment_id = request.json.get("paymentId")
    if not payment_id:
        return jsonify({"error": "Payment ID is required"}), 400

    try:
        # Call the function to approve the payment
        result = approve_payment(payment_id)
        if result["status"] == "success":
            return jsonify({"message": f"Payment {payment_id} approved successfully"}), 200
        else:
            return jsonify({"error": f"Failed to approve payment {payment_id}"}), 500
    except Exception as e:
        print(f"Error approving payment: {e}")
        return jsonify({"error": "Approval failed"}), 500

# Route to complete a payment
@payments_bp.route("/complete", methods=["POST"])
def complete():
    payment_id = request.json.get("paymentId")
    txid = request.json.get("txid")
    if not payment_id or not txid:
        return jsonify({"error": "Payment ID and transaction ID are required"}), 400

    try:
        # Call the function to complete the payment
        result = complete_payment(payment_id, txid)
        if result["status"] == "success":
            return jsonify({"message": f"Payment {payment_id} completed successfully"}), 200
        else:
            return jsonify({"error": f"Failed to complete payment {payment_id}"}), 500
    except Exception as e:
        print(f"Error completing payment: {e}")
        return jsonify({"error": "Completion failed"}), 500

# Route to handle canceled payments
@payments_bp.route("/cancelled_payment", methods=["POST"])
def cancel_payment():
    payment_id = request.json.get("paymentId")
    if not payment_id:
        return jsonify({"error": "Payment ID is required"}), 400

    try:
        # Custom logic for canceled payments
        # You can handle the cancellation of a payment here, depending on your business logic
        return jsonify({"message": f"Payment {payment_id} canceled"}), 200
    except Exception as e:
        print(f"Error canceling payment: {e}")
        return jsonify({"error": "Failed to cancel payment"}), 500