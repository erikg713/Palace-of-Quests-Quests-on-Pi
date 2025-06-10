import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this')
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

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_config(env=None):
    env = env or os.getenv("FLASK_ENV", "production")
    return config_map.get(env, ProductionConfig)


import os

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')

class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_config(env=None):
    env = env or os.getenv("FLASK_ENV", "production")
    return config_map.get(env, ProductionConfig)
