def test_xss_prevention_in_user_input(client):
    malicious_input = "<script>alert('XSS')</script>"
    response = client.post('/api/comments', json={"content": malicious_input})
    assert response.status_code == 400
    assert "Invalid input" in response.json["message"]

def test_xss_in_quest_titles(client, init_database):
    response = client.post('/api/quests', json={"title": "<script>alert('XSS')</script>", "level_required": 5})
    assert response.status_code == 400
    assert "Invalid input" in response.json["message"]
