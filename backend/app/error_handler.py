from flask import jsonify

def register_error_handlers(app):
    """
    Registers error handlers for the Flask app.
    """

    # Handle 400 - Bad Request
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    # Handle 401 - Unauthorized
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({'error': 'Unauthorized', 'message': str(error)}), 401

    # Handle 403 - Forbidden
    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({'error': 'Forbidden', 'message': str(error)}), 403

    # Handle 404 - Not Found
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not Found', 'message': 'The requested resource could not be found.'}), 404

    # Handle 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return jsonify({'error': 'Method Not Allowed', 'message': str(error)}), 405

    # Handle 500 - Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred.'}), 500

    # Handle other unhandled exceptions
    @app.errorhandler(Exception)
    def unhandled_exception(error):
        return jsonify({'error': 'Unhandled Exception', 'message': str(error)}), 500
