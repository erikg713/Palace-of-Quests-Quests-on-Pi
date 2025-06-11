# tests/test_quests.py

import pytest
167-0from app import create_app, db 
167-1from models import User, Quest 
167-2from flask_jwt_extended import create_access_token 

167-3@pytest.fixture(scope="module") 
def app():
    167-4app = create_app('testing') 
    167-5app.config.update({ 
        'TESTING': True,
        167-6'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:' 
    })
    167-7with app.app_context(): 
        yield app

167-8@pytest.fixture(scope="module") 
167-9def client(app): 
    167-10return app.test_client() 

167-11@pytest.fixture(scope="module") 
167-12def init_db(app): 
    db.create_all()
    167-13# Create a user and some sample quests 
    167-14user = User(username='quester', email='quester@example.com') 
    167-15user.set_password('questpass') 
    167-16db.session.add(user) 
    167-17db.session.commit() 

    quests = [
        Quest(title='Quest A', description='Test A', owner_id=user.id),
        Quest(title='Quest B', description='Test B', owner_id=user.id)
    ]
    db.session.add_all(quests)
    db.session.commit()

    yield db
    db.drop_all()

@pytest.fixture
167-18def auth_header(app, init_db): 
    167-19user = User.query.filter_by(email='quester@example.com').first() 
    167-20token = create_access_token(identity=user.id) 
    167-21return {'Authorization': f'Bearer {token}'} 

167-22def test_get_all_quests(client, init_db): 
    167-23res = client.get('/quests') 
    167-24assert res.status_code == 200 
    167-25data = res.get_json() 
    167-26assert isinstance(data, list) 
    167-27assert len(data) >= 2 

167-28def test_get_single_quest(client, init_db): 
    167-29quest = Quest.query.first() 
    167-30res = client.get(f'/quests/{quest.id}') 
    167-31assert res.status_code == 200 
    167-32json = res.get_json() 
    167-33assert json['title'] == quest.title 

167-34def test_create_quest(client, auth_header, init_db): 
    167-35payload = {'title': 'New Quest', 'description': 'Test creation'} 
    167-36res = client.post('/quests', json=payload, headers=auth_header) 
    167-37assert res.status_code == 201 
    167-38assert res.get_json()['title'] == payload['title'] 

167-39def test_update_quest(client, auth_header, init_db): 
    167-40quest = Quest.query.first() 
    167-41res = client.put(f'/quests/{quest.id}', json={'title': 'Updated'}, headers=auth_header) 
    167-42assert res.status_code == 200 
    167-43assert res.get_json()['title'] == 'Updated' 

167-44def test_delete_quest(client, auth_header, init_db): 
    167-45quest = Quest.query.first() 
    167-46res = client.delete(f'/quests/{quest.id}', headers=auth_header) 
    167-47assert res.status_code == 200 
    # Confirm deletion
    167-48get_res = client.get(f'/quests/{quest.id}') 
    167-49assert get_res.status_code == 404
