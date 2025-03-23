# app/models/quest.py
from app import db

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reward = db.Column(db.Float, nullable=False)
    user_quests = db.relationship('UserQuest', backref='quest', lazy=True)

