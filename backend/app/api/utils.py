"""API Utilities: Response Formatting & Error Handling"""

from flask import jsonify

def api_response(success=True, data=None, message=None, status_code=200, **extra):
    resp = {
        "success": success,
        "data": data,
        "message": message,
    }
    resp.update(extra)
    return jsonify(resp), status_code

def api_error(message, status_code=400, **extra):
    return api_response(success=False, data=None, message=message, status_code=status_code, **extra)
