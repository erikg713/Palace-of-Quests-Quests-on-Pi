from flask import Blueprint, request, jsonify
from app.models import PremiumBenefit, User, db
import requests
import os

premium_bp = Blueprint("premium", __name__)

# Initialize a purchase request with Pi coins
@premium_bp.route("/purchase_premium", methods=["POST"])
def purchase_premium():
    data = request.get_json()
    benefit_id = data.get("benefit_id")
    user_id = 1  # Replace with actual user retrieval

    benefit = PremiumBenefit.query.get(benefit_id)
    if not benefit:
        return jsonify({"error": "Benefit not found"}), 404

    # Define Pi Network API payment request
    payment_data = {
        "amount": benefit.price_pi,
        "memo": f"Purchase of {benefit.name}",
        "metadata": {"user_id": user_id, "benefit_id": benefit_id}
    }

    # Call Pi Network API to initiate the payment
    response = requests.post("https://api.minepi.com/v2/payments", json=payment_data, headers={
        "Authorization": f"Bearer {os.getenv('PI_API_KEY')}"
    })

    if response.status_code == 201:
        return jsonify({"message": "Payment initiated", "payment_data": response.json()})
    else:
        return jsonify({"error": "Payment failed"}), 500

# Confirm the purchase after Pi payment is completed
@premium_bp.route("/confirm_purchase", methods=["POST"])
def confirm_purchase():
    data = request.get_json()
    payment_id = data.get("payment_id")
    user_id = 1  # Replace with actual user retrieval

    # Simulate payment verification (use Pi Network webhook or callback for real verification)
    payment_verified = True  # Replace with actual verification logic
    if payment_verified:
        # Apply the benefit to the user
        apply_premium_benefit(user_id, data.get("benefit_id"))
        return jsonify({"message": "Payment confirmed and benefit applied"})
    else:
        return jsonify({"error": "Payment verification failed"}), 400
