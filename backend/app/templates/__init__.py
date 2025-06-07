"""
Custom Jinja2 template package for Pi Network and 3D Metaverse backend.

- Place all HTML templates in this directory.
- Register custom Jinja2 filters and context processors below to enhance template rendering
  for Pi Network-specific features and interactive 3D metaverse experiences.

Example setup for custom template utilities:
"""

from flask import Blueprint

templates_bp = Blueprint('templates', __name__, template_folder='.')

# Example: Register a custom Jinja2 filter for formatting Pi coin values.
def format_pi(value, decimals=4):
    """
    Formats a numeric value as Pi with a fixed number of decimals, e.g., 3.1415 π.
    """
    try:
        return f"{float(value):.{decimals}f} π"
    except (ValueError, TypeError):
        return "0.0000 π"

# Example: Register a context processor for metaverse-specific context.
def metaverse_context():
    """
    Injects global context variables for 3D metaverse templates.
    """
    return {
        "METAVERSE_TITLE": "Palace of Quests 3D",
        "PI_NETWORK_ENABLED": True,
        # Add more global context as needed
    }

# To use these in your Flask app, register them during app setup:
# from . import templates_bp, format_pi, metaverse_context
# app.register_blueprint(templates_bp)
# app.jinja_env.filters['format_pi'] = format_pi
# app.context_processor(metaverse_context)
