# app/models/item.py
from app import db
from typing import Dict


class Item(db.Model):
    """
    Represents an item in the application, with details such as name, description, price, and owner.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(500), nullable=False)  # Limit description to 500 characters
    price = db.Column(db.Float, nullable=False, default=0.0)  # Default price is 0.0
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    owner = db.relationship('User', backref=db.backref('items', cascade='all, delete-orphan'))

    def to_dict(self) -> Dict[str, any]:
        """
        Returns a dictionary representation of the Item object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "owner_id": self.owner_id,
        }

    def update(self, **kwargs):
        """
        Update the fields of the Item object.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
