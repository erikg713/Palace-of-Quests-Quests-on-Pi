# backend/app/payments.py
@app.route("/pay", methods=["POST"])
def process_payment():
    data = request.json
    payment_id = data.get("payment_id")
    
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}
    response = requests.post(f"{PI_AUTH_URL}/payments/{payment_id}", headers=headers)
    
    return jsonify(response.json()), response.status_code
