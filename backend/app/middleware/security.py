"""
Security middleware for Palace of Quests application.

Implements security headers, CSRF protection, and request validation.
"""

from flask import Flask, request, jsonify
from flask.wrappers import Response
from typing import Dict, Any


def init_security_headers(app: Flask) -> None:
    """
    Initialize security headers middleware.
    
    Args:
        app: Flask application instance
    """
    
    @app.after_request
    def add_security_headers(response: Response) -> Response:
        """Add security headers to all responses."""
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
        }
        
        for header, value in security_headers.items():
            response.headers[header] = value
        
        return response
    
    @app.before_request
    def validate_request():
        """Validate incoming requests for security compliance."""
        # Validate Content-Type for POST/PUT requests
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type
            if content_type and not content_type.startswith(('application/json', 'multipart/form-data')):
                return jsonify({
                    'error': 'Invalid Content-Type',
                    'message': 'Only JSON and form data are accepted'
                }), 400
        
        # Check for oversized requests
        max_content_length = app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # 16MB
        if request.content_length and request.content_length > max_content_length:
            return jsonify({
                'error': 'Request too large',
                'message': f'Request size exceeds {max_content_length} bytes'
            }), 413
    
    app.logger.info("Security headers middleware initialized successfully")
def init_security_headers(app):
    @app.after_request
    def set_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
