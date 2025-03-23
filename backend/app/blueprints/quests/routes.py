from flask import render_template, request, redirect, url_for
from flask_login import login_required
from . import quests_bp
from app.models import Quest
from app import db

@quests_bp.route('/')
@login_required
def list_quests():
    quests = Quest.query.all()
    return render_template('quests/list.html', quests=quests)

@quests_bp.route('/<int:quest_id>')
@login_required
def quest_detail(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    return render_template('quests/detail.html', quest=quest)

@quests_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_quest():
    if request.method == 'POST':
        # Create new quest
        # ...
        return redirect(url_for('quests.list_quests'))
    return render_template('quests/create.html')
