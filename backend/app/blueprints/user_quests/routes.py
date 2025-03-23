# app/blueprints/user_quests/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user_quest import UserQuest
from app.blueprints.user_quests.forms import UserQuestForm

user_quests_bp = Blueprint('user_quests', __name__)

@user_quests_bp.route('/')
@login_required
def index():
    user_quests = UserQuest.query.filter_by(user_id=current_user.id).all()
    return render_template('user_quests/index.html', user_quests=user_quests)

@user_quests_bp.route('/accept', methods=['GET', 'POST'])
@login_required
def accept():
    form = UserQuestForm()
    if form.validate_on_submit():
        user_quest = UserQuest(
            user_id=current_user.id,
            quest_id=form.quest_id.data,
            status='accepted'
        )
        db.session.add(user_quest)
        db.session.commit()
        flash('Quest accepted successfully.', 'success')
        return redirect(url_for('user_quests.index'))
    return render_template('user_quests/accept.html', form=form)

