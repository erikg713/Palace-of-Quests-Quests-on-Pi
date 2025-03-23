import logging
from flask import jsonify

def register_error_handlers(app):
    def error_response(error, message, status_code):
        response = jsonify({'error': error, 'message': message})
        response.status_code = status_code
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the exception details for debugging purposes
        app.logger.error("Unhandled Exception", exc_info=e)

        # Customize your error response here
        return error_response("Internal server error", str(e), 500)

    @app.errorhandler(400)
    def bad_request(error):
        return error_response('Bad Request', str(error), 400)

    @app.errorhandler(401)
    def unauthorized(error):
        return error_response('Unauthorized', str(error), 401)

    @app.errorhandler(403)
    def forbidden(error):
        return error_response('Forbidden', str(error), 403)

    @app.errorhandler(404)
    def not_found(error):
        return error_response('Not Found', str(error), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return error_response('Internal Server Error', 'An unexpected error occurred.', 500)
