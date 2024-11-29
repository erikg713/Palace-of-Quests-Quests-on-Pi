from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.avatar_upgrade import AvatarUpgrade
from models.user_inventory import UserInventory, db
from utils.pi_payments import process_shop_payment

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/upgrades", methods=["GET"])
@jwt_required()
def get_upgrades():
    upgrades = AvatarUpgrade.query.all()
    return jsonify([{
        "id": upgrade.id,
        "name": upgrade.name,
        "description": upgrade.description,
        "level_required": upgrade.level_required,
        "price": upgrade.price
    } for upgrade in upgrades]), 200

@shop_bp.route("/purchase", methods=["POST"])
@jwt_required()
def purchase_upgrade():
    identity = get_jwt_identity()
    data = request.json

    upgrade = AvatarUpgrade.query.get(data["upgrade_id"])
    if not upgrade:
        return jsonify({"message": "Upgrade not found"}), 404

    if data["current_level"] < upgrade.level_required:
        return jsonify({"message": "Level too low for this upgrade"}), 400

    success = process_shop_payment(identity["id"], data["transaction_id"], upgrade.price)
    if not success:
        return jsonify({"message": "Payment failed"}), 400

    inventory_item = UserInventory(user_id=identity["id"], upgrade_id=upgrade.id)
    db.session.add(inventory_item)
    db.session.commit()
    return jsonify({"message": "Upgrade purchased successfully"}), 200
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.avatar_upgrade import AvatarUpgrade
from models.user_inventory import UserInventory, db
from utils.pi_payments import process_shop_payment

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/upgrades", methods=["GET"])
@jwt_required()
def get_upgrades():
    upgrades = AvatarUpgrade.query.all()
    return jsonify([{
        "id": upgrade.id,
        "name": upgrade.name,
        "description": upgrade.description,
        "level_required": upgrade.level_required,
        "price": upgrade.price
    } for upgrade in upgrades]), 200

@shop_bp.route("/purchase", methods=["POST"])
@jwt_required()
def purchase_upgrade():
    identity = get_jwt_identity()
    data = request.json

    upgrade = AvatarUpgrade.query.get(data["upgrade_id"])
    if not upgrade:
        return jsonify({"message": "Upgrade not found"}), 404

    if data["current_level"] < upgrade.level_required:
        return jsonify({"message": "Level too low for this upgrade"}), 400

    success = process_shop_payment(identity["id"], data["transaction_id"], upgrade.price)
    if not success:
        return jsonify({"message": "Payment failed"}), 400

    inventory_item = UserInventory(user_id=identity["id"], upgrade_id=upgrade.id)
    db.session.add(inventory_item)
    db.session.commit()
    return jsonify({"message": "Upgrade purchased successfully"}), 200