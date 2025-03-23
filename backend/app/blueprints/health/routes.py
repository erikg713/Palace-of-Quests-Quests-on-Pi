from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/status')
def status():
    return jsonify({'status': 'ok'})

