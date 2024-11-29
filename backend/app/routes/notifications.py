from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize socketio here or in the app.py if you want global access
socketio = SocketIO()

notifications_bp = Blueprint("notifications", __name__)

# Route to send a notification
@notifications_bp.route("/send_notification", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated (optional based on your needs)
def send_notification():
    data = request.get_json()

    # Validate incoming data
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "user_id and message are required"}), 400

    # Optional: Check if user exists (or other custom checks)
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Emit notification to the user's socket
    socketio.emit(f"notification_{user_id}", {"message": message})

    return jsonify({"message": "Notification sent"}), 200