import os

class Config:
    """
    Base configuration with default settings.
    Sensitive information should be set via environment variables.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/pi_users_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "replace-this-with-a-secure-key")
class DevelopmentConfig(Config):
    """
    Configuration for development environment.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'postgresql://postgres:password@db:5432/palace_of_quests')
    DEBUG = True

class TestingConfig(Config):
    """
    Configuration for testing environment.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///test.db')
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """
    Configuration for production environment.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL', 'postgresql://postgres:password@db:5432/palace_of_quests')
    DEBUG = False
    TESTING = False
