from flask import Blueprint, request, jsonify
import requests

payments_bp = Blueprint('payments', __name__)

PI_API_URL = "https://api.minepi.com/v2"
APP_ID = "your_app_id"
APP_SECRET = "your_secret_key"

@payments_bp.route('/api/payments/initiate', methods=['POST'])
def initiate_payment():
    data = request.json
    user_id = data['user_id']
    amount = data['amount']
    payment_type = data['payment_type']

    payload = {
        "amount": amount,
        "memo": payment_type,
        "metadata": {"user_id": user_id},
    }

    headers = {"Authorization": f"Key {APP_SECRET}"}
    response = requests.post(f"{PI_API_URL}/payments", json=payload, headers=headers)

    if response.status_code == 201:
        payment_data = response.json()
        return jsonify(payment_data), 201
    else:
        return jsonify({"message": "Failed to initiate payment"}), 400

@payments_bp.route('/api/payments/confirm', methods=['POST'])
def confirm_payment():
    data = request.json
    payment_id = data['payment_id']
    status = data['status']

    # Verify payment via Pi API
    headers = {"Authorization": f"Key {APP_SECRET}"}
    response = requests.post(f"{PI_API_URL}/payments/{payment_id}/complete", headers=headers)

    if response.status_code == 200 and status == "Completed":
        return jsonify({"message": "Payment confirmed"})
    else:
