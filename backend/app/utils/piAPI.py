import requests
import os

PI_API_BASE_URL = "https://api.minepi.com/v2"
PI_API_KEY = os.getenv("PI_API_KEY")

def approve_payment(payment_id):
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}
    response = requests.post(f"{PI_API_BASE_URL}/payments/{payment_id}/approve", headers=headers)
    response.raise_for_status()
    return response.json()

def complete_payment(payment_id, txid):
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}
    payload = {"txid": txid}
    response = requests.post(f"{PI_API_BASE_URL}/payments/{payment_id}/complete", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

import requests
import os

PI_API_BASE_URL = "https://api.minepi.com/v2"
PI_API_KEY = os.getenv("PI_API_KEY")

def approve_payment(payment_id):
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}
    response = requests.post(f"{PI_API_BASE_URL}/payments/{payment_id}/approve", headers=headers)
    response.raise_for_status()
    return response.json()

def complete_payment(payment_id, txid):
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}
    payload = {"txid": txid}
    response = requests.post(f"{PI_API_BASE_URL}/payments/{payment_id}/complete", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
