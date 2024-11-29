# run.py: Entry point for local development
from app import create_app

# Create the Flask app using the factory pattern
app = create_app()

# For local development
if __name__ == "__main__":
    app.run(debug=True)
