import json

def test_login(client):
    login_data = {"username": "test_user", "password": "password123"}
    response = client.post('/api/auth/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 200
    assert "access_token" in response.json
