from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def init_rate_limiter(app):
    # Initialize the limiter using the request's remote address as key.
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    return limiter
