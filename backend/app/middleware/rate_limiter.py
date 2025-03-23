from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from time import time
from flask import request, jsonify, Flask

def init_rate_limiter(app: Flask) -> Limiter:
    """
    Initialize the rate limiter using the request's remote address as key.
    
    Args:
        app (Flask): The Flask application instance.
        
    Returns:
        Limiter: The initialized Limiter instance.
    """
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    limiter.init_app(app)
    return limiter

class RateLimiterMiddleware:
    """
    Middleware for rate limiting based on client IP address.
    
    Args:
        app (Flask): The Flask application instance.
        limit (int): The number of requests allowed per period.
        period (int): The time period in seconds for rate limiting.
    """
    
    def __init__(self, app: Flask, limit: int = 100, period: int = 60):
        self.app = app
        self.limit = limit
        self.period = period
        self.clients = {}

    def __call__(self, environ: dict, start_response):
        client_ip = environ.get('REMOTE_ADDR')
        current_time = time()

        if client_ip not in self.clients:
            self.clients[client_ip] = []

        request_times = self.clients[client_ip]
        request_times = [t for t in request_times if current_time - t < self.period]
        request_times.append(current_time)
        self.clients[client_ip] = request_times

        if len(request_times) > self.limit:
            res = jsonify({'error': 'rate limit exceeded'})
            res.status_code = 429
            return res(environ, start_response)

        return self.app(environ, start_response)
