class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@db:5432/palace_of_quests"
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@db:5432/palace_of_quests"
    DEBUG = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
