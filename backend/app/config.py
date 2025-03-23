import os

class Config:
    """
    Base configuration with default settings.
    Sensitive information should be set via environment variables.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Configuration for development environment.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'postgresql://postgres:password@db:5432/palace_of_quests')
    DEBUG = True

class TestingConfig(Config):
    """
    Configuration for testing environment.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///test.db')
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """
    Configuration for production environment.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL', 'postgresql://postgres:password@db:5432/palace_of_quests')
    DEBUG = False
    TESTING = False
