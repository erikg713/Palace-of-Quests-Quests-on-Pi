import json

def test_nested_routes(client, init_database):
    response = client.get('/api/players/1/quests')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_quest_completion_flow(client, init_database):
    # Assign quest
    assign_response = client.post('/api/players/1/quests', json={"quest_id": 1})
    assert assign_response.status_code == 200

    # Complete quest
    complete_response = client.post('/api/players/1/quests/1/complete')
    assert complete_response.status_code == 200
    assert complete_response.json["message"] == "Quest completed!"
