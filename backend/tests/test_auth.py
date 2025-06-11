# Test/auth.py

import pytest
from flask import url_for
from app import create_app, db
from models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    # Flask provides a way to test applications by exposing the Werkzeug test Client
    testing_client = flask_app.test_client()

    # Establish an application context
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    # Add a test user
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    yield db

    db.drop_all()


def test_register_user(test_client, init_database):
    response = test_client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpass123'
    })

    assert response.status_code == 201
    assert b"User registered successfully" in response.data


def test_login_user_success(test_client, init_database):
    response = test_client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 200
    assert b"access_token" in response.data


def test_login_user_invalid_password(test_client, init_database):
    response = test_client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert b"Invalid credentials" in response.data


def test_protected_route_requires_token(test_client):
    response = test_client.get('/auth/protected')

    assert response.status_code == 401
    assert b"Missing Authorization Header" in response.data
