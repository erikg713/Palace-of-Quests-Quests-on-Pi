import requests
from flask import request, jsonify, g
from functools import wraps

PI_API_URL = "https://api.minepi.com/v2/me"
APP_ACCESS_TOKEN = "YOUR_PI_APP_ACCESS_TOKEN"  # Store securely, use env var in production

def verify_pi_token(pi_token: str):
    """
    Verify Pi Network access token and return user info if valid.
    """
    headers = {"Authorization": f"Bearer {pi_token}"}
    response = requests.get(PI_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def pi_login_required(f):
    """
    Decorator to require Pi Network authentication for a route.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pi_token = request.headers.get("Authorization")
        if not pi_token or not pi_token.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Pi token"}), 401
        pi_token = pi_token.split(" ", 1)[1]
        user_info = verify_pi_token(pi_token)
        if not user_info:
            return jsonify({"error": "Invalid Pi token"}), 403
        g.pi_user = user_info  # Save user info for use in the route
        return f(*args, **kwargs)
    return decorated_function
import os

# Get PI App access token from environment variable for security.
# Ensure to set 'PI_APP_ACCESS_TOKEN' in your deployment environment.
APP_ACCESS_TOKEN = os.getenv("PI_APP_ACCESS_TOKEN")
if not APP_ACCESS_TOKEN:
    raise RuntimeError(
        "PI_APP_ACCESS_TOKEN environment variable is not set. "
        "Set this variable in your environment configuration."
    )
