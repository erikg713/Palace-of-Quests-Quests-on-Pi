# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Initialize the CORS object
cors = CORS()
