# app/blueprints/economy/forms.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class TransactionForm(FlaskForm):
    recipient_id = IntegerField('Recipient User ID', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

