import requests
import os

PI_SDK_API_KEY = os.getenv("PI_SDK_API_KEY")

def verify_payment(payment_id):
    url = f"https://api.minepi.com/v2/payments/{payment_id}"
    headers = {"Authorization": f"Bearer {PI_SDK_API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"verified": False}