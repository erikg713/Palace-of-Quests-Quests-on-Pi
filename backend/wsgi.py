import os
from app import create_app
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# Fetch environment settings (development by default)
env = os.getenv("FLASK_ENV", "development")

# Initialize the Flask application using the factory function
app = create_app(env)

if __name__ == "__main__":
    # For local development, run the Flask app directly
    app.run(host="0.0.0.0", port=5000, debug=(env == "development"))
