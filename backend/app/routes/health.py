from flask import Blueprint, jsonify, current_app, make_response
from datetime import datetime, timezone

health_bp = Blueprint('health', __name__)

@health_bp.route('/status', methods=['GET'])
def health_status():
    """
    Health check endpoint for service monitoring.
    Returns status, UTC timestamp, and environment info.
    """
    try:
        utc_now = datetime.now(timezone.utc).isoformat()
        response = {
            "status": "ok",
            "timestamp": utc_now,
            "service": current_app.config.get("SERVICE_NAME", "Palace of Quests"),
            "environment": current_app.config.get("ENV", "development"),
            "version": current_app.config.get("VERSION", "1.0.0"),
        }
        resp = make_response(jsonify(response), 200)
        resp.headers["Cache-Control"] = "no-store"
        resp.headers["Content-Type"] = "application/json"
        return resp
    except Exception as e:
        current_app.logger.exception("Health check failed")
        error_resp = {
            "status": "error",
            "message": "Internal Server Error"
        }
        return jsonify(error_resp), 500
