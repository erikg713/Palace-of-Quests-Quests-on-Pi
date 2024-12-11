def test_sql_injection_protection(client):
    malicious_input = "' OR 1=1; --"
    response = client.post('/api/auth/login', json={"username": malicious_input, "password": "password123"})
    assert response.status_code == 401
    assert "Invalid credentials" in response.json["message"]

def test_xss_protection(client):
    malicious_script = "<script>alert('XSS')</script>"
    response = client.post('/api/comments', json={"content": malicious_script})
    assert response.status_code == 400
    assert "Invalid input" in response.json["message"]
