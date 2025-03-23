from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.user import User
from app.blueprints.admin.forms import UserForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users')
@login_required
def list_users():
    """
    Route to list all users.
    """
    users = User.query.all()
    return render_template('admin/list_users.html', users=users)

@admin_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """
    Route to edit user details.
    """
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()
            flash('User updated successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('admin.list_users'))
    return render_template('admin/edit_user.html', form=form, user=user)
