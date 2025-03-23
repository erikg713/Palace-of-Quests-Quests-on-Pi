from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.quest import Quest
from app.blueprints.quests import quests_bp
from app.blueprints.quests.forms import QuestForm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@quests_bp.route('/')
@login_required
def index():
    try:
        quests = Quest.query.with_entities(Quest.id, Quest.title, Quest.description, Quest.reward).all()
        return render_template('quests/index.html', quests=quests)
    except Exception as e:
        logger.error(f"Error fetching quests: {e}")
        flash('An error occurred while fetching quests.', 'danger')
        return redirect(url_for('main.index'))

@quests_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestForm()
    if form.validate_on_submit():
        try:
            quest = Quest(title=form.title.data, description=form.description.data, reward=form.reward.data)
            db.session.add(quest)
            db.session.commit()
            flash('Quest created successfully.', 'success')
            return redirect(url_for('quests.index'))
        except Exception as e:
            logger.error(f"Error creating quest: {e}")
            db.session.rollback()
            flash('An error occurred while creating the quest.', 'danger')
    return render_template('quests/create.html', form=form)

@quests_bp.route('/<int:quest_id>')
@login_required
def detail(quest_id):
    try:
        quest = Quest.query.get_or_404(quest_id)
        return render_template('quests/detail.html', quest=quest)
    except Exception as e:
        logger.error(f"Error fetching quest detail: {e}")
        flash('An error occurred while fetching the quest details.', 'danger')
        return redirect(url_for('quests.index'))
