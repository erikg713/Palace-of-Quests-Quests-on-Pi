import logging
from flask import Blueprint, jsonify
from models import User, Transaction, UserQuest, db
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

# Constants
COMPLETED_STATUS = 'completed'
DAYS_TRACKED = 7

# Configure module-level logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@analytics_bp.route('/overview', methods=['GET'])
def overview():
    """
    Get platform-wide summary analytics.
    Returns total users, total transactions, total Pi spent, and total quests completed.
    """
    try:
        total_users = User.query.count()
        total_transactions = Transaction.query.count()
        total_pi_spent = db.session.query(db.func.sum(Transaction.amount)).scalar() or 0.0
        total_quests_completed = UserQuest.query.filter_by(status=COMPLETED_STATUS).count()

        response = {
            'total_users': total_users,
            'total_transactions': total_transactions,
            'total_pi_spent': total_pi_spent,
            'total_quests_completed': total_quests_completed
        }
        logger.info("Fetched overview analytics: %r", response)
        return jsonify(response), 200
    except Exception as exc:
        logger.error("Error fetching overview analytics: %s", exc)
        return jsonify({'error': 'Internal server error'}), 500

@analytics_bp.route('/daily', methods=['GET'])
def daily_stats():
    """
    Get daily analytics for the previous 7 days (including today):
    - New users
    - Transactions
    - Quests completed
    Returned as a list ordered by day descending (most recent first).
    """
    try:
        today = datetime.utcnow().date()
        range_start = datetime(today.year, today.month, today.day) - timedelta(days=DAYS_TRACKED - 1)
        range_end = datetime(today.year, today.month, today.day) + timedelta(days=1)

        # Bulk fetch to minimize DB queries
        all_users = User.query.filter(User.created_at >= range_start, User.created_at < range_end).all()
        all_transactions = Transaction.query.filter(Transaction.created_at >= range_start, Transaction.created_at < range_end).all()
        all_quests = UserQuest.query.filter(UserQuest.completed_at >= range_start, UserQuest.completed_at < range_end).all()

        results = []
        for i in range(DAYS_TRACKED):
            day = today - timedelta(days=i)
            day_start = datetime(day.year, day.month, day.day)
            day_end = day_start + timedelta(days=1)

            users_count = sum(1 for user in all_users if day_start <= user.created_at < day_end)
            transactions_count = sum(1 for txn in all_transactions if day_start <= txn.created_at < day_end)
            quests_count = sum(1 for quest in all_quests if day_start <= quest.completed_at < day_end)

            results.append({
                'date': day.isoformat(),
                'new_users': users_count,
                'transactions': transactions_count,
                'quests_completed': quests_count
            })

        logger.info("Fetched daily analytics for %d days.", DAYS_TRACKED)
        return jsonify({'daily_stats': results}), 200
    except Exception as exc:
        logger.error("Error fetching daily analytics: %s", exc)
        return jsonify({'error': 'Internal server error'}), 500
