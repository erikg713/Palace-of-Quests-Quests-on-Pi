from flask import Blueprint, request, jsonify
from app.utils.piAPI import approve_payment, complete_payment

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/approve", methods=["POST"])
def approve():
    payment_id = request.json.get("paymentId")
    try:
        result = approve_payment(payment_id)
        return jsonify({"message": f"Payment {payment_id} approved successfully"})
    except Exception as e:
        return jsonify({"error": "Approval failed"}), 500

@payments_bp.route("/complete", methods=["POST"])
def complete():
    payment_id = request.json.get("paymentId")
    txid = request.json.get("txid")
    try:
        result = complete_payment(payment_id, txid)
        return jsonify({"message": f"Payment {payment_id} completed successfully"})
    except Exception as e:
        return jsonify({"error": "Completion failed"}), 500

@payments_bp.route("/cancelled_payment", methods=["POST"])
def cancel_payment():
    payment_id = request.json.get("paymentId")
    # Handle custom logic for canceled payments if needed
    return jsonify({"message": f"Payment {payment_id} canceled"})

from flask import Blueprint, request, jsonify
from .utils import piAPI

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/approve", methods=["POST"])
def approve():
    payment_id = request.json.get("paymentId")
    try:
        piAPI.approve_payment(payment_id)
        return jsonify({"message": "Payment approved"})
    except Exception as e:
        return jsonify({"error": "Approval failed"}), 500

@payments_bp.route("/complete", methods=["POST"])
def complete():

@payments_bp.route("/approve", methods=["POST"])
def approve_payment():
    payment_id = request.json.get("paymentId")
    response = requests.post(
        f"https://api.minepi.com/v2/payments/{payment_id}/approve",
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
    if response.status_code == 200:
        return jsonify({"message": f"Approved payment {payment_id}"})
    else:
        return jsonify({"error": "Approval failed"}), response.status_code
@payments_bp.route("/complete", methods=["POST"])
def complete_payment():
    payment_id = request.json.get("paymentId")
    txid = request.json.get("txid")
    response = requests.post(
        f"https://api.minepi.com/v2/payments/{payment_id}/complete",
        json={"txid": txid},
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
    if response.status_code == 200:
        return jsonify({"message": f"Completed payment {payment_id}"})
    else:
        return jsonify({"error": "Completion failed"}), response.status_code
@payments_bp.route("/cancelled_payment", methods=["POST"])
def cancel_payment():
    payment_id = request.json.get("paymentId")
    # Custom cancellation handling logic here
    return jsonify({"message": f"Payment {payment_id} canceled"})

from flask import Blueprint, request, jsonify
from app.utils.piAPI import approve_payment, complete_payment

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/approve", methods=["POST"])
def approve():
    payment_id = request.json.get("paymentId")
    try:
        result = approve_payment(payment_id)
        return jsonify(result)
    except Exception as e:
        print(f"Error approving payment: {e}")
        return jsonify({"error": "Failed to approve payment"}), 500

@payments_bp.route("/complete", methods=["POST"])
def complete():
    payment_id = request.json.get("paymentId")
    txid = request.json.get("txid")
    try:
        result = complete_payment(payment_id, txid)
        return jsonify(result)
    except Exception as e:
        print(f"Error completing payment: {e}")
        return jsonify({"error": "Failed to complete payment"}), 500

from flask import Blueprint, request, jsonify
from app.models import PremiumBenefit, User, db
from app.utils import apply_premium_benefit
import requests
import os

premium_bp = Blueprint("premium", __name__)

@premium_bp.route("/benefits", methods=["GET"])
def get_premium_benefits():
    benefits = PremiumBenefit.query.all()
    return jsonify([benefit.to_dict() for benefit in benefits])

@premium_bp.route("/purchase_premium", methods=["POST"])
def purchase_premium():
    data = request.get_json()
    benefit_id = data.get("benefit_id")
    user_id = data.get("user_id")  # Make sure to retrieve user ID from authenticated session

    benefit = PremiumBenefit.query.get(benefit_id)
    if not benefit:
        return jsonify({"error": "Benefit not found"}), 404

    payment_data = {
        "amount": benefit.price_pi,
        "memo": f"Purchase of {benefit.name}",
        "metadata": {"user_id": user_id, "benefit_id": benefit_id}
    }

    try:
        response = requests.post("https://api.minepi.com/v2/payments", json=payment_data, headers={
            "Authorization": f"Bearer {os.getenv('PI_API_KEY')}"
        })
        response.raise_for_status()  # Raise an error if request fails
        return jsonify({"message": "Payment initiated", "payment_data": response.json()})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Payment initiation failed", "details": str(e)}), 500

@premium_bp.route("/confirm_purchase", methods=["POST"])
def confirm_purchase():
    data = request.get_json()
    payment_id = data.get("payment_id")
    benefit_id = data.get("benefit_id")
    user_id = data.get("user_id")

    # Simulate verification - replace with actual Pi Network verification logic
    payment_verified = verify_payment(payment_id)
    if payment_verified:
        apply_premium_benefit(user_id, benefit_id)
        return jsonify({"message": "Payment confirmed and benefit applied"})
    else:
        return jsonify({"error": "Payment verification failed"}), 400

def verify_payment(payment_id):
    # Placeholder function for actual Pi Network verification logic
    # Replace this with real Pi Network callback or webhook verification
    return True
