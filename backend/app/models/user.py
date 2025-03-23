# app/models/user.py

from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    Represents a user in the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    quests = db.relationship('UserQuest', backref='user', lazy=True)
    transactions_sent = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender', lazy=True)
    transactions_received = db.relationship('Transaction', foreign_keys='Transaction.recipient_id', backref='recipient', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
