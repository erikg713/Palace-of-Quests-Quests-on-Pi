import pytest
from app import create_app, db
from app.models import Player, Quest

@pytest.fixture
def app():
    """Create and configure a new app instance for tests."""
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
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Initialize the database with mock data."""
    with app.app_context():
        player = Player(username="test_user", level=5)
        quest = Quest(title="Find the Hidden Key", level_required=3)
        db.session.add(player)
        db.session.add(quest)
        db.session.commit()
        yield db
