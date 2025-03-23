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
# app/middleware/rate_limiter.py
from time import time
from flask import request, jsonify

class RateLimiterMiddleware:
    def __init__(self, app, limit=100, period=60):
        self.app = app
        self.limit = limit
        self.period = period
        self.clients = {}

    def __call__(self, environ, start_response):
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
