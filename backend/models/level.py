from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
