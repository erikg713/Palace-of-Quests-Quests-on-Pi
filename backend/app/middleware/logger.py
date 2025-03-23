import logging
from flask import request, g
import time
# app/middleware/logger.py
from flask import request

def log_request():
    def middleware():
        app.logger.info(f'{request.method} {request.path}')
    return middleware

def setup_logging(app):
    # Set up logging handler if not already present
    if not app.logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
    
    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        if not hasattr(g, 'start'):
            g.start = time.time()
        duration = time.time() - g.start
        method = request.method
        path = request.path
        status = response.status_code
        app.logger.info(f'{method} {path} {status} {duration:.3f}s')
        return response
