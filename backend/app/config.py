import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    PI_API_KEY = os.getenv("PI_API_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
