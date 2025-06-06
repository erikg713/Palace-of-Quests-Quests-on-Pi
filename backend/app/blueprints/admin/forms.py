# app/blueprints/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

class UserForm(FlaskForm):
    """
    Form for updating user profile information in the admin panel.
    """
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Please enter a username."),
            Length(min=2, max=20, message="Username must be 2-20 characters."),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message="Username can only contain letters, numbers, and underscores."
            )
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Please enter your email address."),
            Email(message="Please enter a valid email address.")
        ]
    )
    submit = SubmitField('Update')
