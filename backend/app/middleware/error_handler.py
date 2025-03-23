import logging
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the exception details for debugging purposes
        app.logger.error("Unhandled Exception", exc_info=e)
        
        # Customize your error response here
        response = {
            "error": "Internal server error",
            "message": str(e)
        }
        return jsonify(response), 500
