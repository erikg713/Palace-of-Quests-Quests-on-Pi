import os

class Config:
    """Base configuration with default settings. 
    Sensitive values should always be set via environment variables."""
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    PI_AUTH_URL = "https://api.minepi.com/v2"
    REQUEST_TIMEOUT = 5

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    JSONIFY_PRETTYPRINT_REGULAR = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

def get_config(config_name):
    if config_name == "development":
        return DevelopmentConfig
    return ProductionConfig
    @staticmethod
    def validate():
        if not Config.SECRET_KEY:
            raise RuntimeError("SECRET_KEY environment variable must be set for security.")
        if not Config.SQLALCHEMY_DATABASE_URI:
            raise RuntimeError("DATABASE_URL environment variable must be set for database connection.")

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", "postgresql://postgres:password@db:5432/palace_of_quests")
    DEBUG = True

class TestingConfig(Config):
    """Configuration for testing environment."""
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///test.db")
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Configuration for production environment."""
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL")
    DEBUG = False
    TESTING = False

    @staticmethod
    def validate():
        if not os.getenv("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY must be set as an environment variable in production.")
        if not os.getenv("PROD_DATABASE_URL"):
            raise RuntimeError("PROD_DATABASE_URL must be set as an environment variable for production database.")

# Optional: Environment-based config selection
config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)
