from flask import jsonify, request
from app.models import QuestProgress, db
from flask_jwt_extended import jwt_required, get_jwt_identity

@auth.route('/quests/progress', methods=['POST'])
@jwt_required()
def update_quest_progress():
    user_id = get_jwt_identity()
    data = request.get_json()

    quest_progress = QuestProgress.query.filter_by(user_id=user_id, quest_id=data['quest_id']).first()
    if not quest_progress:
        quest_progress = QuestProgress(user_id=user_id, quest_id=data['quest_id'])
        db.session.add(quest_progress)

    quest_progress.progress = data.get('progress', quest_progress.progress)
    quest_progress.completed = data.get('completed', quest_progress.completed)
    db.session.commit()

    return jsonify({"message": "Quest progress updated", "progress": quest_progress.progress}), 200

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"username": user.username, "email": user.email}), 200
from flask import Blueprint, jsonify

# Create blueprint for main routes
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message": "Welcome to Palace of Quests!"})

@main.route("/status")
def status():
    return jsonify({"status": "running", "service": "backend"})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Quest, User

quest = Blueprint('quest', __name__)

@quest.route('/quests', methods=['POST'])
@jwt_required()
def create_quest():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_quest = Quest(
        title=data['title'],
        description=data['description'],
        reward=data['reward'],
        created_by=user_id
    )
    db.session.add(new_quest)
    db.session.commit()
    return jsonify({"message": "Quest created successfully"}), 201

@quest.route('/quests', methods=['GET'])
def get_all_quests():
    quests = Quest.query.all()
    output = []
    for quest in quests:
        quest_data = {
            "id": quest.id,
            "title": quest.title,
            "description": quest.description,
            "reward": quest.reward,
            "created_at": quest.created_at
        }
        output.append(quest_data)
    return jsonify({"quests": output}), 200

@quest.route('/quests/<int:quest_id>', methods=['GET'])
def get_single_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    return jsonify({
        "id": quest.id,
        "title": quest.title,
        "description": quest.description,
        "reward": quest.reward,
        "created_at": quest.created_at
    }), 200

@quest.route('/quests/<int:quest_id>', methods=['PUT'])
@jwt_required()
def update_quest(quest_id):
    user_id = get_jwt_identity()
    quest = Quest.query.get_or_404(quest_id)
    if quest.created_by != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    quest.title = data['title']
    quest.description = data['description']
    quest.reward = data['reward']
    db.session.commit()
    return jsonify({"message": "Quest updated successfully"}), 200

@quest.route('/quests/<int:quest_id>', methods=['DELETE'])
@jwt_required()
def delete_quest(quest
@auth.route('/quests/reward', methods=['POST'])
@jwt_required()
def reward_user():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    quest = Quest.query.get(data['quest_id'])
    if not user or not quest:
        return jsonify({"message": "Invalid user or quest"}), 400

    # Distribute reward if quest is completed
    if data.get('completed', False):
        user.add_xp(quest.reward)
        db.session.commit()
        return jsonify({"message": f"Reward added! New level: {user.level}, XP: {user.xp}"}), 200

    return jsonify({"message": "Quest not completed"}), 400
