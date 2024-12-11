def test_get_quest(client):
    response = client.get('/api/quests/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
