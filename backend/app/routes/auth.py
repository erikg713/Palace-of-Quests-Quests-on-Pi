from flask import Blueprint, request, jsonify, current_app
import requests

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('', methods=['POST'])
def authenticate():
    data = request.get_json(silent=True)
    if not data or "access_token" not in data:
        return jsonify({"error": "Missing access_token"}), 400

    user_token = data["access_token"]
    pi_api_url = current_app.config["PI_AUTH_URL"]

    try:
        response = requests.get(
            f"{pi_api_url}/me",
            headers={"Authorization": f"Bearer {user_token}"},
            timeout=current_app.config["REQUEST_TIMEOUT"]
        )
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.HTTPError as e:
        current_app.logger.warning(f"Pi API error: {e}")
        return jsonify({"error": "Authentication failed"}), 401
    except Exception as e:
        current_app.logger.error(f"Pi API unavailable: {e}")
        return jsonify({"error": "Pi API unavailable"}), 503



from flask import Blueprint, request, jsonify, current_app
import requests

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("", methods=["POST"])
def authenticate():
    """
    Authenticate user via Pi Network.
    """
    data = request.get_json(silent=True)
    if not data or "access_token" not in data:
        return jsonify({"error": "Missing access_token in request body"}), 400

    user_token = data["access_token"]
    pi_api_url = current_app.config.get("PI_AUTH_URL")
    timeout = current_app.config.get("REQUEST_TIMEOUT", 5)
    
    try:
        response = requests.get(
            f"{pi_api_url}/me",
            headers={"Authorization": f"Bearer {user_token}"},
            timeout=timeout
        )
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.HTTPError as http_err:
        current_app.logger.warning(f"Pi API authentication failed: {http_err}")
        return jsonify({"error": "Authentication failed", "detail": str(http_err)}), 401
    except requests.RequestException as req_err:
        current_app.logger.error(f"Request to Pi API failed: {req_err}")
        return jsonify({"error": "Pi API unavailable", "detail": str(req_err)}), 503
