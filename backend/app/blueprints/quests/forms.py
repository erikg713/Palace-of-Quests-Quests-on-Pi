from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class QuestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    reward = IntegerField('Reward', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Create Quest')
