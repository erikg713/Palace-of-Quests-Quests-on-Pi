from flask import Blueprint, render_template
from flask_login import login_required
from app.models.user import User

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/')
@login_required
def index():
    user_count = User.query.count()
    return render_template('analytics/index.html', user_count=user_count)

