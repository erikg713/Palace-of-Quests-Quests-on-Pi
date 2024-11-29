from flask import Blueprint, jsonify
from flask_caching import Cache

marketplace_bp = Blueprint('marketplace', __name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})

@marketplace_bp.route('/items', methods=['GET'])
@cache.cached(timeout=300)  # Cache items for 5 minutes
def get_items():
    items = Inventory.query.all()
    return jsonify([{'id': item.id, 'name': item.item_name, 'type': item.item_type, 'price': item.price} for item in items])
