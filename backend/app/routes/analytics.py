from flask import Blueprint, request, jsonify
from models import User, Transaction, UserQuest, db
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/overview', methods=['GET'])
def overview():
    total_users = User.query.count()
    total_transactions = Transaction.query.count()
    total_pi_spent = db.session.query(db.func.sum(Transaction.amount)).scalar() or 0.0
    total_quests_completed = UserQuest.query.filter_by(status='completed').count()

    data = {
        'total_users': total_users,
        'total_transactions': total_transactions,
        'total_pi_spent': total_pi_spent,
        'total_quests_completed': total_quests_completed
    }
    return jsonify(data), 200

@analytics_bp.route('/daily', methods=['GET'])
def daily_stats():
    # Get stats for the past 7 days
    today = datetime.utcnow().date()
    results = []
    for i in range(7):
        day = today - timedelta(days=i)
        day_start = datetime(day.year, day.month, day.day)
        day_end = day_start + timedelta(days=1)
        
        users_created = User.query.filter(User.created_at >= day_start, User.created_at < day_end).count()
        transactions = Transaction.query.filter(Transaction.created_at >= day_start, Transaction.created_at < day_end).count()
        quests_completed = UserQuest.query.filter(UserQuest.completed_at >= day_start, UserQuest.completed_at < day_end).count()
        
        results.append({
            'date': day.isoformat(),
            'new_users': users_created,
            'transactions': transactions,
            'quests_completed': quests_completed
        })
    return jsonify({'daily_stats': results}), 200
