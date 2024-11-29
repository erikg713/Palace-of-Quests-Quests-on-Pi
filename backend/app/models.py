# Database models 
from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.JSON, default={})
    experience_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Level(db.Model):
    __tablename__ = "levels"
    level_id = db.Column(db.Integer, primary_key=True)
    level_number = db.Column(db.Integer, unique=True, nullable=False)
    experience_required = db.Column(db.Integer, nullable=False)
    reward = db.Column(db.JSON, default={})

class Upgrade(db.Model):
    __tablename__ = "upgrades"
    upgrade_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Integer, nullable=False)
    available_from_level = db.Column(db.Integer, nullable=False)

class Subscription(db.Model):
    __tablename__ = "subscriptions"
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    subscription_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.String(20), default="Pending")
from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.JSON, default={})
    experience_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Level(db.Model):
    __tablename__ = "levels"
    level_id = db.Column(db.Integer, primary_key=True)
    level_number = db.Column(db.Integer, unique=True, nullable=False)
    experience_required = db.Column(db.Integer, nullable=False)
    reward = db.Column(db.JSON, default={})

class Upgrade(db.Model):
    __tablename__ = "upgrades"
    upgrade_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Integer, nullable=False)
    available_from_level = db.Column(db.Integer, nullable=False)

class Subscription(db.Model):
    __tablename__ = "subscriptions"
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    subscription_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.String(20), default="Pending")