from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from app.models import MarketplaceItem, db

marketplace_bp = Blueprint('marketplace', __name__)
ma = Marshmallow()

# Marshmallow schema for MarketplaceItem
class MarketplaceItemSchema(ma.Schema):
    name = fields.String(required=True, error_messages={"required": "Name is required."})
    description = fields.String(required=True, error_messages={"required": "Description is required."})
    price = fields.Float(required=True, error_messages={"required": "Price is required."})
    seller_id = fields.Integer(dump_only=True)  # Automatically populated from JWT identity

item_schema = MarketplaceItemSchema()
items_schema = MarketplaceItemSchema(many=True)

# Route to get all items in the marketplace
@marketplace_bp.route('/items', methods=['GET'])
def get_items():
    items = MarketplaceItem.query.all()
    return jsonify(items_schema.dump(items)), 200

# Route to add a new item to the marketplace
@marketplace_bp.route('/items', methods=['POST'])
@jwt_required()
def add_item():
    current_user = get_jwt_identity()
    try:
        # Validate request data
        data = item_schema.load(request.json)
        new_item = MarketplaceItem(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            seller_id=current_user
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item added successfully'}), 201
    except ValidationError as ve:
        return jsonify({'errors': ve.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to update an item
@marketplace_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    current_user = get_jwt_identity()
    item = MarketplaceItem.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item not found'}), 404
    if item.seller_id != current_user:
        return jsonify({'error': 'Unauthorized action'}), 403

    try:
        data = item_schema.load(request.json, partial=True)  # Allow partial updates
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.price = data.get('price', item.price)
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'}), 200
    except ValidationError as ve:
        return jsonify({'errors': ve.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to delete an item
@marketplace_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    current_user = get_jwt_identity()
    item = MarketplaceItem.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item not found'}), 404
    if item.seller_id != current_user:
        return jsonify({'error': 'Unauthorized action'}), 403

    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
