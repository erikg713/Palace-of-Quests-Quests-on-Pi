from flask import Blueprint, jsonify

# Create blueprint for main routes
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message": "Welcome to Palace of Quests!"})

@main.route("/status")
def status():
    return jsonify({"status": "running", "service": "backend"})
