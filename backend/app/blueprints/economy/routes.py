from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.transaction import Transaction
from app.blueprints.economy.forms import TransactionForm

economy_bp = Blueprint('economy', __name__)

@economy_bp.route('/')
@login_required
def index():
    # Use eager loading to reduce the number of queries
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('economy/index.html', transactions=transactions)

@economy_bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            sender_id=current_user.id,
            recipient_id=form.recipient_id.data,
            amount=form.amount.data,
            description=form.description.data
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction completed successfully.', 'success')
        return redirect(url_for('economy.index'))
    return render_template('economy/transfer.html', form=form)
