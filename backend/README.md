Palace of Quests Backend

This is the backend service for Palace of Quests, a Web3 application integrating the Pi Network SDK to enable secure transactions and user authentication. It is built with Flask and supports PostgreSQL as the database.


---

Features

RESTful API: Provides endpoints for frontend interaction.

JWT Authentication: Ensures secure user sessions.

Pi Network Payment Integration: Handles Pi coin transactions via the Pi Network SDK.

PostgreSQL Support: Robust database for data storage.

Dockerized Deployment: Simplifies environment setup and scaling.



---

Prerequisites

Before setting up the backend, ensure you have the following:

Python: v3.9+ installed.

PostgreSQL: Database instance running.

Docker: Optional but recommended for containerized deployment.

Pi Network App credentials from the Pi Developer Portal.



---

Installation

1. Clone the Repository:

git clone https://github.com/your-repo/palace-of-quests-backend.git
cd palace-of-quests-backend


2. Create a Virtual Environment:

python3 -m venv venv
source venv/bin/activate


3. Install Dependencies:

pip install -r requirements.txt


4. Set Up the .env File: Create a .env file in the root directory with the following keys:

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_random_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/palace_of_quests
PI_APP_ID=your_pi_app_id
PI_API_KEY=your_pi_api_key

Replace placeholders with your actual configuration.


5. Initialize the Database: Run migrations to set up the database schema:

flask db upgrade




---

Development

1. Run the Development Server:

flask run

The server will start at http://localhost:5000.


2. Testing Endpoints: Use tools like Postman or cURL to interact with the API.




---

API Endpoints

Authentication

POST /auth/register: Register a new user.

POST /auth/login: Authenticate and return a JWT.


Payments

POST /payment/initiate: Start a Pi coin transaction.

POST /payment/complete: Confirm a transaction.


Quests

GET /quests: Fetch all quests.

POST /quests: Add a new quest.



---

Docker Deployment

1. Build the Docker Image:

docker build -t palace-of-quests-backend .


2. Run the Container:

docker run -p 5000:5000 --env-file .env palace-of-quests-backend


3. Using Docker-Compose: If you have a docker-compose.yml file, start the service:

docker-compose up




---

Deployment

Hosting Platforms

The backend can be deployed on platforms like:

AWS EC2 or Lightsail

Heroku

Google Cloud

DigitalOcean


Ensure you set the environment variables on the hosting platform to match your .env file.


---

Contributing

1. Fork the repository.


2. Create a new branch:

git checkout -b feature/your-feature


3. Commit your changes and push to the branch.


4. Open a pull request.


backend/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── player.py
│   │   ├── challenges.py
│   │   ├── marketplace.py
│   │   ├── payments.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── jwt_utils.py
│   │   ├── pi_network_sdk.py
│   └── config.py
├── migrations/
├── tests/
│   ├── test_auth.py
│   ├── test_player.py
│   ├── test_marketplace.py
├── wsgi.py
├── requirements.txt
└── run.py
---

License

This project is licensed under the MIT License.


---

Feel free to ask for adjustments or more advanced sections like testing, monitoring, or CI/CD!

