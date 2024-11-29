from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    wallet_address = db.Column(db.String(100), nullable=False)

class Quest(db.Model):
    __tablename__ = 'quests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    txid = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    wallet_address = db.Column(db.String(100), nullable=False)

class Avatar(db.Model):
    __tablename__ = 'avatars'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='avatar', lazy=True)

class Quest(db.Model):
    __tablename__ = 'quests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    reward_points = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    equipped = db.Column(db.Boolean, default=False)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatars.id'))

from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    wallet_address = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "wallet_address": self.wallet_address
        }

class LevelReward(db.Model):
    __tablename__ = 'level_rewards'
    level = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(100))
    reward_description = db.Column(db.Text)
    stat_boost = db.Column(db.Integer, default=0)
    item_unlock = db.Column(db.String(100))
    quest_difficulty = db.Column(db.Integer)

    def to_dict(self):
        return {
            "level": self.level,
            "reward_name": self.reward_name,
            "reward_description": self.reward_description,
            "stat_boost": self.stat_boost,
            "item_unlock": self.item_unlock,
            "quest_difficulty": self.quest_difficulty
        }

