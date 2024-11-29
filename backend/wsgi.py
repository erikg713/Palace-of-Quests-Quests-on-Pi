# WSGI configuration for Palace of Quests on PythonAnywhere

import sys

# Add the project directory to the system path
sys.path.insert(0, '/home/Dev713/PalaceOfQuests')

# Import the application factory and create the app
from app import create_app
application = create_app()  # Flask expects `application` as the callable
