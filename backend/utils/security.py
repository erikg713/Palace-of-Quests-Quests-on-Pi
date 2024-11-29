from flask import Flask, request, jsonify
from app import app
from datetime import datetime, timedelta

@app.route('/login', methods=["POST"])
def login():
    # Assuming user authentication has been handled
    user_id = 1  # Example: Replace with actual user ID after login validation
    payload = {'user_id': user_id}
    
    # Create JWT for authenticated user
    token = create_jwt(payload)
    
    # Send the token in the response (you could also store it in cookies)
    response = jsonify({"message": "Login successful"})
    response.set_cookie('access_token', token)  # Store token in cookies
    return response

@app.route('/protected', methods=["GET"])
@jwt_required
def protected():
    # If we get here, the JWT is valid and the user is authenticated
    return jsonify({"message": "This is a protected route"})