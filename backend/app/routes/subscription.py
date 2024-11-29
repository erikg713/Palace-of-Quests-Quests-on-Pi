from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from .models import db, User, UserProgress

# Blueprint for subscription routes
subscription_bp = Blueprint('subscription', __name__)

# Subscription plans
PREMIUM_DURATION_DAYS = 365  # 1 year

# Subscription Model
class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    plan = db.Column(db.String, nullable=False)  # Example: "premium"
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, default='active')  # active, expired, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Route: Subscribe to a plan
@subscription_bp.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    verified_uid = data.get('uid')  # UID from Pi Platform /me API
    plan = data.get('plan', 'premium')  # Default plan is "premium"

    # Validate user
    user = User.query.filter_by(uid=verified_uid).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if user already has an active subscription
    existing_subscription = Subscription.query.filter_by(user_id=user.id, status='active').first()
    if existing_subscription:
        return jsonify({'error': 'User already has an active subscription'}), 400

    # Create new subscription
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=PREMIUM_DURATION_DAYS)
    subscription = Subscription(user_id=user.id, plan=plan, start_date=start_date, end_date=end_date, status='active')
    db.session.add(subscription)
    db.session.commit()

    return jsonify({
        'message': 'Subscription created successfully',
        'subscription_id': subscription.id,
        'plan': subscription.plan,
        'start_date': subscription.start_date,
        'end_date': subscription.end_date
    }), 200

# Route: Check subscription status
@subscription_bp.route('/subscription-status', methods=['POST'])
def subscription_status():
    data = request.json
    verified_uid = data.get('uid')  # UID from Pi Platform /me API

    # Validate user
    user = User.query.filter_by(uid=verified_uid).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get user's active subscription
    subscription = Subscription.query.filter_by(user_id=user.id, status='active').first()
    if not subscription:
        return jsonify({'status': 'no_active_subscription'}), 200

    # Check if the subscription has expired
    if subscription.end_date < datetime.utcnow():
        subscription.status = 'expired'
        db.session.commit()
        return jsonify({'status': 'expired'}), 200

    return jsonify({
        'status': 'active',
        'plan': subscription.plan,
        'end_date': subscription.end_date
    }), 200

# Route: Cancel subscription
@subscription_bp.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    data = request.json
    verified_uid = data.get('uid')  # UID from Pi Platform /me API

    # Validate user
    user = User.query.filter_by(uid=verified_uid).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Cancel the user's active subscription
    subscription = Subscription.query.filter_by(user_id=user.id, status='active').first()
    if not subscription:
        return jsonify({'error': 'No active subscription to cancel'}), 404

    subscription.status = 'canceled'
    db.session.commit()
    return jsonify({'message': 'Subscription canceled successfully'}), 200
