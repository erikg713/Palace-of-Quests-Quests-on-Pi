# Database models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    uid = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    level = db.Column(db.Integer, default=1)
    experience_points = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
from database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=  True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    wallet_address = db.Column(db.String(128), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Establish relationship with Inventory
    inventory_items = db.relationship('Inventory', backref='owner', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Inventory {self.item_name} (Type: {self.item_type})>"
