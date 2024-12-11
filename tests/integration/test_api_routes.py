import json

def test_get_quests(client):
    response = client.get('/api/quests')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_post_new_quest(client):
    new_quest = {
        "title": "Defeat the Dragon",
        "level_required": 15
    }
    response = client.post('/api/quests', data=json.dumps(new_quest), content_type='application/json')
    assert response.status_code == 201
    assert response.json["title"] == "Defeat the Dragon"
