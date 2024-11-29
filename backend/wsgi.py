from app import create_app

# Initialize the Flask app using the factory pattern
app = create_app()

if __name__ == "__main__":
    # Run the Flask development server (optional, mostly used locally)
    app.run(host="0.0.0.0", port=5000)
