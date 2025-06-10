"""
Centralized error handling with detailed logging and user-friendly responses.
Includes custom exceptions for different error types and monitoring integration.

Author: Senior Backend Team  
Last Modified: 2025-06-04
"""

import traceback
import sys
from typing import Dict, Any, Optional, Tuple
from flask import Flask, request, jsonify, g
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized, Forbidden, NotFound
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError
import sentry_sdk

from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Not found"), 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Server Error: {e}")
        return jsonify(error="Internal server error"), 500
class BusinessLogicError(Exception):
    """Base exception for business logic errors."""
    def __init__(self, message: str, code: str = None, status_code: int = 400):
        self.message = message
        self.code = code or 'BUSINESS_LOGIC_ERROR'
        self.status_code = status_code
        super().__init__(message)


class QuestNotFoundError(BusinessLogicError):
    """Raised when a quest cannot be found."""
    def __init__(self, quest_id: int):
        super().__init__(f"Quest with ID {quest_id} not found", 'QUEST_NOT_FOUND', 404)


class InsufficientFundsError(BusinessLogicError):
    """Raised when user has insufficient funds for transaction."""
    def __init__(self, required: float, available: float):
        message = f"Insufficient funds. Required: {required}, Available: {available}"
        super().__init__(message, 'INSUFFICIENT_FUNDS', 402)


class QuestAlreadyCompletedError(BusinessLogicError):
    """Raised when attempting to complete an already completed quest."""
    def __init__(self, quest_id: int):
        super().__init__(f"Quest {quest_id} is already completed", 'QUEST_COMPLETED', 409)


def register_error_handlers(app: Flask) -> None:
    """Register comprehensive error handlers for the application."""
    
    def log_error(error: Exception, extra_context: Dict = None) -> None:
        """Log error with request context and stack trace."""
        context = {
            'method': request.method,
            'url': request.url,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'request_id': getattr(g, 'request_id', 'unknown'),
            'user_id': getattr(g, 'user_id', 'anonymous'),
        }
        
        if extra_context:
            context.update(extra_context)
        
        app.logger.error(
            f"Error occurred: {str(error)}\n"
            f"Context: {context}\n"
            f"Traceback: {traceback.format_exc()}"
        )
    
    def create_error_response(
        message: str, 
        error_type: str = 'error',
        status_code: int = 500,
        details: Dict = None
    ) -> Tuple[Dict[str, Any], int]:
        """Create standardized error response."""
        response = {
            'success': False,
            'error': {
                'type': error_type,
                'message': message,
                'timestamp': g.get('start_time', 0),
                'request_id': getattr(g, 'request_id', 'unknown')
            }
        }
        
        if details:
            response['error']['details'] = details
        
        # Include stack trace in development
        if app.debug and hasattr(sys, '_getframe'):
            response['error']['debug_info'] = traceback.format_stack()[-3:-1]
        
        return response, status_code
    
    # HTTP Error Handlers
    @app.errorhandler(400)
    def handle_bad_request(error: BadRequest):
        log_error(error)
        return create_error_response(
            'Invalid request format or parameters',
            'bad_request',
            400
        )
    
    @app.errorhandler(401)
    def handle_unauthorized(error: Unauthorized):
        return create_error_response(
            'Authentication required or invalid credentials',
            'unauthorized',
            401
        )
    
    @app.errorhandler(403)
    def handle_forbidden(error: Forbidden):
        log_error(error, {'reason': 'access_forbidden'})
        return create_error_response(
            'Access forbidden. Insufficient permissions',
            'forbidden',
            403
        )
    
    @app.errorhandler(404)
    def handle_not_found(error: NotFound):
        return create_error_response(
            'The requested resource was not found',
            'not_found',
            404
        )
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return create_error_response(
            f'Method {request.method} not allowed for this endpoint',
            'method_not_allowed',
            405
        )
    
    @app.errorhandler(429)
    def handle_too_many_requests(error):
        return create_error_response(
            'Rate limit exceeded. Please slow down your requests',
            'rate_limit_exceeded',
            429
        )
    
    # Database Error Handlers
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error: SQLAlchemyError):
        log_error(error, {'error_type': 'database_error'})
        
        # Rollback any pending transactions
        from app import db
        db.session.rollback()
        
        if isinstance(error, IntegrityError):
            return create_error_response(
                'Data integrity constraint violated',
                'integrity_error',
                409,
                {'constraint': str(error.orig) if hasattr(error, 'orig') else None}
            )
        
        return create_error_response(
            'Database operation failed',
            'database_error',
            500
        )
    
    # Validation Error Handler
    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        log_error(error, {'validation_errors': error.messages})
        return create_error_response(
            'Request validation failed',
            'validation_error',
            400,
            {'field_errors': error.messages}
        )
    
    # Business Logic Error Handlers
    @app.errorhandler(BusinessLogicError)
    def handle_business_logic_error(error: BusinessLogicError):
        log_error(error, {'business_error_code': error.code})
        return create_error_response(
            error.message,
            error.code.lower(),
            error.status_code
        )
    
    @app.errorhandler(QuestNotFoundError)
    def handle_quest_not_found(error: QuestNotFoundError):
        return create_error_response(
            error.message,
            'quest_not_found',
            404
        )
    
    @app.errorhandler(InsufficientFundsError)
    def handle_insufficient_funds(error: InsufficientFundsError):
        log_error(error, {'error_type': 'payment_error'})
        return create_error_response(
            error.message,
            'insufficient_funds',
            402
        )
    
    # Generic Exception Handler
    @app.errorhandler(Exception)
    def handle_generic_exception(error: Exception):
        log_error(error, {'error_type': 'unhandled_exception'})
        
        # Send to monitoring service (Sentry, etc.)
        if hasattr(app, 'sentry') or 'sentry_sdk' in sys.modules:
            sentry_sdk.capture_exception(error)
        
        # Don't expose internal errors in production
        if app.debug:
            return create_error_response(
                f'Internal server error: {str(error)}',
                'internal_error',
                500,
                {'exception_type': type(error).__name__}
            )
        else:
            return create_error_response(
                'An unexpected error occurred. Please try again later.',
                'internal_error',
                500
            )
    
    # Request parsing errors
    @app.errorhandler(UnicodeDecodeError)
    def handle_unicode_error(error):
        log_error(error, {'error_type': 'encoding_error'})
        return create_error_response(
            'Invalid character encoding in request',
            'encoding_error',
            400
        )
    
    app.logger.info("Error handling middleware initialized successfully")
