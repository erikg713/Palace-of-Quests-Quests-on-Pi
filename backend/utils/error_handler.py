import logging
from flask import jsonify
from app import app

# Set up logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

@app.errorhandler(400)
def bad_request(error):
    app.logger.error(f"Bad Request: {error}")
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(404)
def not_found(error):
    app.logger.error(f"Not Found: {error}")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f"Internal Server Error: {error}")
    return jsonify({"error": "An unexpected error occurred"}), 500