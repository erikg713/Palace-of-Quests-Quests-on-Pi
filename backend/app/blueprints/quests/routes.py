# app/blueprints/quests/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.quest import Quest
from app.blueprints.quests import quests_bp
from app.blueprints.quests.forms import QuestForm

@quests_bp.route('/')
@login_required
def index():
    quests = Quest.query.all()
    return render_template('quests/index.html', quests=quests)

@quests_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestForm()
    if form.validate_on_submit():
        quest = Quest(title=form.title.data, description=form.description.data, reward=form.reward.data)
        db.session.add(quest)
        db.session.commit()
        flash('Quest created successfully.', 'success')
        return redirect(url_for('quests.index'))
    return render_template('quests/create.html', form=form)

@quests_bp.route('/<int:quest_id>')
@login_required
def detail(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    return render_template('quests/detail.html', quest=quest)

