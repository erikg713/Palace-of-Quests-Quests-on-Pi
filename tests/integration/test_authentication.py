import json
import time

def test_login_and_logout(client, init_database):
    login_data = {"username": "test_user", "password": "password123"}
    login_response = client.post('/api/auth/login', json=login_data)
    assert login_response.status_code == 200
    token = login_response.json["access_token"]

    logout_response = client.post('/api/auth/logout', headers={"Authorization": f"Bearer {token}"})
    assert logout_response.status_code == 200
    assert logout_response.json["message"] == "Logged out successfully"

def test_token_expiration(client, init_database):
    login_data = {"username": "test_user", "password": "password123"}
    login_response = client.post('/api/auth/login', json=login_data)
    assert login_response.status_code == 200
    token = login_response.json["access_token"]

    # Simulate token expiration
    time.sleep(2)  # Adjust based on token expiration settings
    protected_response = client.get('/api/protected', headers={"Authorization": f"Bearer {token}"})
    assert protected_response.status_code == 401

def test_login(client):
    login_data = {"username": "test_user", "password": "password123"}
    response = client.post('/api/auth/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 200
    assert "access_token" in response.json
