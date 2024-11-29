from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.user import User, db

class AuthService:
    @staticmethod
    def register_user(username, password):
        if User.query.filter_by(username=username).first():
            return False
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return True

    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return access_token
        return None
