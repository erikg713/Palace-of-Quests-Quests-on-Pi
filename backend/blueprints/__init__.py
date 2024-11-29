from flask import Flask
from .blueprints.quests import quests

def create_app():
    app = Flask(__name__)
    app.register_blueprint(quests, url_prefix='/api')
    return app
