import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import create_app, db
from app.models import Player, Quest

@pytest.fixture(scope="session")
def app() -> Flask:
    """
    Create and configure a Flask app instance for testing.
    """
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    Returns a test client for the Flask app.
    """
    return app.test_client()

@pytest.fixture
def init_database(app: Flask):
    """
    Seed the in-memory database with initial data for tests.
    """
    with app.app_context():
        player = Player(username="test_user", level=5)
        quest = Quest(title="Find the Hidden Key", level_required=3)
        db.session.add_all([player, quest])
        db.session.commit()
        yield db
        db.session.rollback()
        db.drop_all()
        db.create_all()
