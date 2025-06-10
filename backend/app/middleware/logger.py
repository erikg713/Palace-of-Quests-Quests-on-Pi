"""
Enhanced logging middleware for Palace of Quests application.

Provides structured logging with request tracking, performance monitoring,
and configurable log levels.
"""

import logging
import time
import uuid
from typing import Optional, Dict, Any
from flask import Flask, request, g, jsonify
from flask.wrappers import Response
from werkzeug.exceptions import HTTPException


class RequestFormatter(logging.Formatter):
    """Custom formatter that includes request context in log messages."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with request context."""
        if hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = 'N/A'
        
        if hasattr(g, 'user_id'):
            record.user_id = g.user_id
        else:
            record.user_id = 'anonymous'
        
        return super().format(record)


def setup_logging(app: Flask) -> None:
    """
    Configure application logging with request tracking and performance monitoring.
    
    Args:
        app: Flask application instance
    """
    # Configure log level based on environment
    log_level = logging.DEBUG if app.debug else logging.INFO
    
    # Create formatter
    formatter = RequestFormatter(
        '[%(asctime)s] %(levelname)s [%(request_id)s] [%(user_id)s] '
        '%(name)s: %(message)s'
    )
    
    # Configure file handler for production
    if not app.debug:
        file_handler = logging.FileHandler('palace_quests.log')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    
    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    
    app.logger.setLevel(log_level)
    
    # Request tracking middleware
    @app.before_request
    def before_request():
        """Initialize request tracking."""
        g.request_id = str(uuid.uuid4())[:8]
        g.start_time = time.time()
        
        # Log request details
        app.logger.info(
            f"Request started: {request.method} {request.path} "
            f"from {request.remote_addr}"
        )
    
    @app.after_request
    def after_request(response: Response) -> Response:
        """Log request completion and performance metrics."""
        duration = time.time() - g.start_time
        
        app.logger.info(
            f"Request completed: {response.status_code} "
            f"in {duration:.3f}s"
        )
        
        # Add request ID to response headers for debugging
        response.headers['X-Request-ID'] = g.request_id
        
        return response
    import logging

def setup_logging(app):
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Logging middleware initialized")
    app.logger.info("Logging middleware initialized successfully")
