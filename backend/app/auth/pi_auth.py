import os
import requests
from flask import request, jsonify, g
from functools import wraps
import logging

# Constants
PI_API_URL = "https://api.minepi.com/v2/me"
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Securely get the PI App access token from an environment variable
APP_ACCESS_TOKEN = os.getenv("PI_APP_ACCESS_TOKEN")
if not APP_ACCESS_TOKEN:
    raise RuntimeError(
        "PI_APP_ACCESS_TOKEN environment variable is not set. "
        "Set this variable in your environment configuration."
    )

def verify_pi_token(pi_token: str):
    """
    Verify Pi Network access token and return user info if valid.

    Args:
        pi_token (str): The Pi Network access token.

    Returns:
        dict: User information if the token is valid.
        None: If the token is invalid or an error occurs.
    """
    headers = {"Authorization": f"Bearer {pi_token}"}
    try:
        response = requests.get(PI_API_URL, headers=headers, timeout=5)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error verifying Pi token: {e}")
        return None

def pi_login_required(f):
    """
    Decorator to require Pi Network authentication for a route.

    Args:
        f (function): The route handler function.

    Returns:
        function: The decorated route handler function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pi_token = request.headers.get("Authorization")
        if not pi_token or not pi_token.startswith("Bearer "):
            logger.warning("Missing or invalid Pi token in request headers.")
            return jsonify({"error": "Missing or invalid Pi token"}), HTTP_UNAUTHORIZED

        # Extract the token from the "Bearer " prefix
        pi_token = pi_token.split(" ", 1)[1]
        user_info = verify_pi_token(pi_token)
        if not user_info:
            logger.warning("Invalid Pi token.")
            return jsonify({"error": "Invalid Pi token"}), HTTP_FORBIDDEN

        # Save user info for use in the route
        g.pi_user = user_info
        return f(*args, **kwargs)

    return decorated_function
