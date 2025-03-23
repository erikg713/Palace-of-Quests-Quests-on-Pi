# app/blueprints/transactions/routes.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.transaction import Transaction

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/')
@login_required
def index():
    transactions = Transaction.query.filter(
        (Transaction.sender_id == current_user.id) | 
        (Transaction.recipient_id == current_user.id)
    ).all()
    return render_template('transactions/index.html', transactions=transactions)

