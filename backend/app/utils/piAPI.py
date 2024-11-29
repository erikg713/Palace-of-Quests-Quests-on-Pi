import requests
import os

PI_API_BASE_URL = "https://api.minepi.com/v2"
PI_API_KEY = os.getenv("PI_API_KEY")

def make_payment_request(endpoint, payment_id, data=None):
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}
    url = f"{PI_API_BASE_URL}/payments/{payment_id}/{endpoint}"

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def approve_payment(payment_id):
    return make_payment_request("approve", payment_id)

def complete_payment(payment_id, txid):
    return make_payment_request("complete", payment_id, {"txid": txid})