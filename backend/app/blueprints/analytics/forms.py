# backend/app/blueprints/analytics/forms.py

"""
Forms for Analytics Blueprint
Author: Erik G. - Palace of Quests Team
Last Updated: 2025-06-06

Define WTForms classes related to analytics features here.
"""

from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired

class DateRangeForm(FlaskForm):
    """
    Form for filtering analytics data by date range.
    """
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    submit = SubmitField("Filter")

# Add more analytics forms below as needed
