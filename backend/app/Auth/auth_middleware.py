from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from typing import Callable, Any

def auth_required(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to require JWT authentication for Flask routes.

    Args:
        fn: The function to wrap.

    Returns:
        A wrapped function that verifies JWT authentication.
    """
    @wraps(fn)  # Preserve the original function's metadata
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            # Unauthorized response on JWT validation failure
            return jsonify({
                "error": "Unauthorized access",
                "message": str(e)
            }), 401
    return wrapper

def get_current_user() -> str:
    """
    Retrieves the current user's identity from the JWT.

    Returns:
        The user identity as a string.
    """
    return get_jwt_identity()