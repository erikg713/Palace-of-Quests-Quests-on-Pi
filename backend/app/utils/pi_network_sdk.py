import requests
import os

PI_NETWORK_API_URL = os.getenv("PI_NETWORK_API_URL", "https://api.minepi.com")
PI_NETWORK_SDK_KEY = os.getenv("PI_NETWORK_SDK_KEY")

def create_payment(user_uid, amount, metadata=None):
    """
    Initiates a payment request to the Pi Network.
    """
    url = f"{PI_NETWORK_API_URL}/payments"
    headers = {
        "Authorization": f"Key {PI_NETWORK_SDK_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "user_uid": user_uid,
        "amount": amount,
        "metadata": metadata or {},
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Payment creation failed: {response.json()}")

def verify_payment(payment_id):
    """
    Verifies the status of a payment using its payment_id.
    """
    url = f"{PI_NETWORK_API_URL}/payments/{payment_id}"
    headers = {
        "Authorization": f"Key {PI_NETWORK_SDK_KEY}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Payment verification failed: {response.json()}")
