from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

class UserQuestForm(FlaskForm):
    quest_id = IntegerField('Quest ID', validators=[DataRequired()])
    submit = SubmitField('Accept Quest')

