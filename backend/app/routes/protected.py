from flask import Blueprint, jsonify, g
from app.auth.pi_auth import pi_login_required

bp = Blueprint("protected", __name__)

@bp.route("/api/private-data")
@pi_login_required
def private_data():
    user = g.pi_user
    return jsonify({
        "message": f"Welcome, Pi user {user['username']}",
        "user_id": user['uid']
    })
