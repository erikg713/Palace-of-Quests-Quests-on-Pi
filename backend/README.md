Backend README (Flask)

Overview

The backend of PiQuest is a Flask RESTful API designed to handle user authentication, game mechanics, and marketplace transactions. It interacts with the PostgreSQL database, manages JWT-based authentication, and provides endpoints for user data, items, and quests.

Installation

1. Clone the Repository:

git clone https://github.com/username/piquest-backend.git
cd piquest-backend


2. Set Up a Virtual Environment:

python3 -m venv venv
source venv/bin/activate


3. Install Dependencies:

pip install -r requirements.txt


4. Set Up Environment Variables: Create a .env file and add the following environment variables:

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=<your_secret_key>
DATABASE_URL=<your_database_url>


5. Run the Application:

flask run



Project Structure

piquest-backend/
├── app/
│   ├── __init__.py           # Initializes Flask app and database
│   ├── models.py             # Database models
│   ├── routes/
│   │   ├── auth.py           # Authentication routes
│   │   ├── marketplace.py     # Marketplace routes
│   │   └── quests.py         # Game quest routes
│   ├── utils/
│   │   ├── security.py       # Password hashing and JWT functions
│   ├── database.py           # Database connection and setup
├── migrations/               # Database migrations for PostgreSQL
├── requirements.txt          # Backend dependencies
├── run.py                    # Entry point for the Flask application
└── README.md

Explanation of Key Files

app/__init__.py: Initializes the Flask application and configures database connections.

app/models.py: Defines database models like User, Inventory, and Quest.

app/routes/auth.py: Handles user authentication (register, login, profile).

app/routes/marketplace.py: Routes for browsing and purchasing items in the marketplace.

app/routes/quests.py: Manages game quests and rewards.

database.py: Connects to the PostgreSQL database and applies models.

utils/security.py: Handles password hashing, verification, and JWT creation.
