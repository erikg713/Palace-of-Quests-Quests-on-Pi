import logging
from flask import request, g
import time

class LoggerMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()
        request_method = environ.get('REQUEST_METHOD')
        path_info = environ.get('PATH_INFO')

        def custom_start_response(status, headers, exc_info=None):
            response_time = time.time() - start_time
            log_details = {
                'method': request_method,
                'path': path_info,
                'status': status.split(' ')[0],
                'response_time': f'{response_time:.4f}s'
            }
            logging.info(log_details)  # Use logging instead of print
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

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
