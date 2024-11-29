from flask import Blueprint, jsonify
from flask_socketio import SocketIO, emit
from app.models import User

notifications_bp = Blueprint("notifications", __name__)
socketio = SocketIO()

@notifications_bp.route("/send_notification", methods=["POST"])
def send_notification():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    # Emit notification to the user's socket
    socketio.emit(f"notification_{user_id}", {"message": message})
    return jsonify({"message": "Notification sent"})
