from flask import Blueprint, render_template

quests = Blueprint('quests', __name__, template_folder='templates')

@quests.route('/quests')
def show_quests():
    return render_template('quests.html')
